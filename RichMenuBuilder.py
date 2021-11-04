
from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    RichMenuAlias,
)

from linebot.models.actions import (
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    RichMenuSwitchAction,
    URIAction,
)

from TextConstant import *


def rich_menu_object_a_json():
    return {
        "size": {
            "width": 2500,
            "height": 1406
        },
        "selected": False,
        "name": "richmenu-a",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 2110,
                    "y": 0,
                    "width": 390,
                    "height": 1406
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-b",
                    "data": "richmenu-changed-to-b"
                }
            },
            {
                "bounds": {
                    "x": 390,
                    "y": 0,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type": "message",
                    "label": "Hello",
                    "text": "Hello"
                }
            },
            {
                "bounds": {
                    "x": 1250,
                    "y": 0,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type": "message",
                    "label": "ByeBye",
                    "text": "ByeBye"
                }
            },
            {
                "bounds": {
                    "x": 390,
                    "y": 703,
                    "width": 860,
                    "height": 703
                },
                "action": {
                     "type": "uri",
                     "label": "Google",
                     "uri": "https://google.com"
                }
            },
            {
                "bounds": {
                    "x": 1250,
                    "y": 703,
                    "width": 860,
                    "height": 703
                },
                "action": {
                     "type": "uri",
                     "label": "CyberLink",
                     "uri": "https://www.cyberlink.com/"
                }
            },
        ]
    }


def rich_menu_object_b_json():
    return {
        "size": {
            "width": 2500,
            "height": 1406
        },
        "selected": False,
        "name": "richmenu-b",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 390,
                    "height": 1406
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-a",
                    "data": "richmenu-changed-to-a"
                }
            },
            {
                "bounds": {
                    "x": 390,
                    "y": 0,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type":"datetimepicker",
                    "label":"Select date",
                    "data":"storeId=12345",
                    "mode":"date",
                }
            },
            {
                "bounds": {
                    "x": 1250,
                    "y": 0,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type": "message",
                    "label": 'GET_REPLY',
                    "text": GET_MESSAGE_DELIVERY_REPLY
                }
            },
            {
                "bounds": {
                    "x": 390,
                    "y": 703,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type": "message",
                    "label": 'FLEX_MESSAGE',
                    "text": FLEX_MESSAGE_DEMO
                }
            },
            {
                "bounds": {
                    "x": 1250,
                    "y": 703,
                    "width": 860,
                    "height": 703
                },
                "action": {
                    "type": "message",
                    "label": 'QUICK_REPLY',
                    "text": QUICK_REPLY_DEMO
                }
            },
        ]
    }

def create_action(action):
    if action['type'] == 'uri':
        return URIAction(type=action['type'], label=action.get('label'), uri=action.get('uri'))
    elif action['type'] == 'message':
        return MessageAction(type=action['type'], label=action.get('label'), text=action.get('text'))
    elif action['type'] == 'datetimepicker':
        return DatetimePickerAction(type=action['type'], label=action.get('label'), data=action.get('data'), mode=action.get('mode'))
    elif action['type'] == 'camera':
        return CameraAction(type=action['type'], label=action.get('label'))
    elif action['type'] == 'cameraRoll':
        return CameraRollAction(type=action['type'], label=action.get('label'))
    elif action['type'] == 'location':
        return LocationAction(type=action['type'], label=action.get('label'))
    else:
        return RichMenuSwitchAction(
            type=action['type'],
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )

def make_rich_menu(line_bot_api):
    # 2. Create rich menu A (richmenu-a)
    rich_menu_object_a = rich_menu_object_a_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_a['areas']
    ]

    rich_menu_to_a_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_a['size']['width'], height=rich_menu_object_a['size']['height']),
        selected=rich_menu_object_a['selected'],
        name=rich_menu_object_a['name'],
        chat_bar_text=rich_menu_object_a['name'],
        areas=areas
    )

    rich_menu_a_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_a_create)

    # 3. Upload image to rich menu A
    with open('./img/richmenu-0.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_a_id, 'image/png', f)

    # 4. Create rich menu B (richmenu-b)
    rich_menu_object_b = rich_menu_object_b_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_b['areas']
    ]

    rich_menu_to_b_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_b['size']['width'], height=rich_menu_object_b['size']['height']),
        selected=rich_menu_object_b['selected'],
        name=rich_menu_object_b['name'],
        chat_bar_text=rich_menu_object_b['name'],
        areas=areas
    )

    rich_menu_b_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_b_create)

    # 5. Upload image to rich menu B
    with open('./img/richmenu-1.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_b_id, 'image/png', f)

    # 6. Set rich menu A as the default rich menu
    line_bot_api.set_default_rich_menu(rich_menu_a_id)

    # 7. Create rich menu alias A
    alias_a = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-a',
        rich_menu_id=rich_menu_a_id
    )
    line_bot_api.create_rich_menu_alias(alias_a)

    # 8. Create rich menu alias B
    alias_b = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-b',
        rich_menu_id=rich_menu_b_id
    )
    line_bot_api.create_rich_menu_alias(alias_b)

if __name__ == '__main__':
    from linebot import LineBotApi
    from secret import *
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    
    menu_list_response = line_bot_api.get_rich_menu_list()
    for m in menu_list_response:
        line_bot_api.delete_rich_menu(m.rich_menu_id)
        
    alias_list_response = line_bot_api.get_rich_menu_alias_list()
    for a in alias_list_response.aliases:
        line_bot_api.delete_rich_menu_alias(a.rich_menu_alias_id)
    
    make_rich_menu(line_bot_api)
