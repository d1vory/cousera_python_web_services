from __future__ import absolute_import, unicode_literals
from celery import task
import requests
import json
import os

from .models import Setting
from django.conf import settings
from django.core.mail import EmailMessage,send_mail


def get_sensors_data(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()['data']


def parse_sensors_data(data):
    return {sensor['name']: sensor['value'] for sensor in data}


@task()
def smart_home_manager():
    data = get_sensors_data(settings.SMART_HOME_API_URL, settings.SMART_HOME_ACCESS_TOKEN)
    parsed_data = parse_sensors_data(data)
    # parsed_data = {'air_conditioner': False, 'bedroom_light': False, 'smoke_detector': False, 'bedroom_presence': True, 'bedroom_motion': True,
    #                'boiler': True, 'cold_water': False, 'hot_water': False, 'bathroom_light': True,
    #                'bathroom_motion': True, 'bathroom_presence': False, 'curtains': 'close', 'washing_machine': 'on', 'bedroom_temperature': 26,
    #                'boiler_temperature': 24, 'leak_detector': False, 'outdoor_light': 94}

    devices_to_update = check_sensors(parsed_data)

    if devices_to_update:

        save_devices_update(devices_to_update)

    return


def save_devices_update(controllers):
    headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
    post_data = [{'name': name, 'value': value} for name, value in controllers.items()]
    response = requests.post(settings.SMART_HOME_API_URL, data=json.dumps({'controllers': post_data}), headers=headers)


def update_device(data, output_dict, device_name, new_value):
    if data[device_name] != new_value or device_name in output_dict:
        output_dict[device_name] = new_value


def check_sensors(data):
    # import pdb
    # pdb.set_trace()
    devices_to_update = {}
    bedroom_target_temperature = Setting.objects.get(controller_name='bedroom_target_temperature').value
    hot_water_target_temperature = Setting.objects.get(controller_name='hot_water_target_temperature').value



    # should boiler be turned on
    if not data['boiler'] and data['boiler_temperature'] <= 0.9*hot_water_target_temperature:
        update_device(data, devices_to_update, 'boiler', True)

    # should boiler be turned off
    if data['boiler'] and data['boiler_temperature'] >= 1.1 * hot_water_target_temperature:
        update_device(data, devices_to_update, 'boiler', False)

    if data['bedroom_temperature'] >= 1.1*bedroom_target_temperature:
        update_device(data, devices_to_update, 'air_conditioner', True)

    if  data['air_conditioner'] and  data['bedroom_temperature'] <= 0.9*bedroom_target_temperature:
        update_device(data, devices_to_update, 'air_conditioner', False)

    # if curtains are automatic
    if data['curtains'] != "slightly_open":
        if data['outdoor_light'] < 50 and not data['bedroom_light']:
            update_device(data, devices_to_update, 'curtains', 'open')
        elif data['outdoor_light'] > 50 or data['bedroom_light']:
            update_device(data, devices_to_update, 'curtains', 'close')

    # if cold water is closed
    if not data['cold_water']:
        update_device(data, devices_to_update, 'boiler', False)
        update_device(data, devices_to_update, 'washing_machine', 'off')

    if data['leak_detector']:
        update_device(data, devices_to_update, 'cold_water', False)
        update_device(data, devices_to_update, 'hot_water', False)
        update_device(data, devices_to_update, 'boiler', False)
        update_device(data, devices_to_update, 'washing_machine', 'off')

        email = EmailMessage('leak detector', 'text', settings.EMAIL_HOST, [settings.EMAIL_RECEPIENT])
        email.send(fail_silently=True)

    # if smoke detected
    if data['smoke_detector']:
        update_device(data, devices_to_update, 'air_conditioner', False)
        update_device(data, devices_to_update, 'bedroom_light', False)
        update_device(data, devices_to_update, 'bathroom_light', False)
        update_device(data, devices_to_update, 'boiler', False)
        update_device(data, devices_to_update, 'washing_machine', 'off')

    # for device_name in devices_to_update.keys():
    #     if data[device_name] == devices_to_update[device_name]:
    #         del devices_to_update[device_name]

    return {k : v for k,v in devices_to_update.items() if data[k] != devices_to_update[k]}
