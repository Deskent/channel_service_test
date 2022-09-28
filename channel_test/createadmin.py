from django.contrib.auth.models import User

admin_name = 'channel_admin'
admin_password = 'channel_password'
if not User.objects.filter(username=admin_name).first():
    User.objects.create_superuser(admin_name, '', admin_password)
    print("Superuser created:"
          f"\nName: {admin_name}"
          f"\nPassword: {admin_password}")
