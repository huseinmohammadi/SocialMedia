from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


def profile_image(instance, filename):
    return "%s/%s/%s" % ('profile', instance.username, filename)


class User(AbstractUser):
    cellphone = models.CharField(max_length=255, null=True, blank=True)
    privet = models.BooleanField(default=False)
    age = models.DateTimeField(null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=profile_image, null=True, blank=True)
    report_count = models.IntegerField(default=0)
    ban = models.BooleanField(default=False)

    @staticmethod
    def get_friends(request):
        request_user_owner = RequestUser.objects.filter(owner=request.user, deleted=False, status=True).values(
            'user_id')
        request_user_user = RequestUser.objects.filter(user=request.user, deleted=False, status=True).values('owner_id')
        request_user = request_user_owner.union(request_user_user, all=True)
        return User.objects.filter(id__in=request_user, is_active=True)

    def login(self, request):
        if self.is_active:
            login(request, self)
            return True
        return False

    def ban_user(self):
        self.ban = True
        self.save()

    def ban_user_count(self):
        if self.report_count == 10:
            self.ban_user()
        else:
            return 0


class Report(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_owner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_user")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def report_user(self):
        self.user.report_count += 1
        self.user.save()


class RequestUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_owner")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="request_user")
    status = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def friends(self):
        if not self.user.privet:
            friends = Friends(request_user=self)
            friends.save()
            self.status = True
            self.save()

    def set_friend(self):
        friend = Friends(request_user=self)
        friend.save()

    def remove_friend(self):
        try:
            friend = Friends.objects.get(request_user=self)
            friend.delete()
            self.status = False
            self.save()
            return 1
        except:
            return 0

    def delete(self, *args, **kwargs):
        self.deleted = True
        super(RequestUser, self).save()


class Friends(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    request_user = models.OneToOneField(RequestUser, on_delete=models.CASCADE, related_name="friends_request")
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.deleted = True
        super(Friends, self).save()
