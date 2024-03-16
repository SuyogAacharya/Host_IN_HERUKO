from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse  # Import reverse here
from django.utils.text import slugify
from django.db.models.signals import pre_save

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    author_profile = models.ImageField(upload_to="media/author")
    name = models.CharField(max_length=100, null=True)
    author_title=models.CharField(max_length=50, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="media/featured_img", null=True)
    featured_video = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    Deadline = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    Certificate = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_details", kwargs={'slug': self.slug})  # Correct indentation

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)

class What_you_learn(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    points = models.CharField (max_length=500)

    def __str__(self):
        return self.points

class Requirements(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    points = models.CharField (max_length=500)

    def __str__(self):
        return self.points

class Lesson (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField (max_length=200)

    def __str__(self):
        return self.name+ "-" + self.course.title


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # This seems unusual, double check if you intend to have two Course foreign keys here
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models. BooleanField (default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username + "-" + self.course.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')
    whatsapp_link = models.URLField()

    def __str__(self):
        return self.name
#student profile model
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self):
      if self.user.username:
        return self.user.username
      else:
        return f"Profile of {self.user}"  # Fallback message
#notice model
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# for about us model
class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='')

class Vision(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='')

class History(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='') 
# for quiz model

class quiz(models.Model):
    quiz_title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.quiz_title
    





