import os
import django
from django.test import TestCase
from sign.models import Event, Guest
django.setup()
os.environ.update({"DJANGO_SETTINGS_MODULE": "guest.settings"})

# Create your tests here.
class ModeTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address='shenzhen', startTime='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realName='alen',
                             phone='13711001101', email='alen@mail.com', sign=False)

    def test_event(self):
            result = Event.objects.get(name="oneplus 3 event")
            self.assertEqual(result.address, "shenzhen")

    def test_guest(self):
            result = Guest.objects.get(phone="13711001101")
            self.assertFalse(result.sign)

#  在命令行执行python manage.py test sign可以成功，
# 但是右键运行执行报错提示:django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
