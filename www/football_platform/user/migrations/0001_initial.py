# Generated by Django 4.1.2 on 2022-11-08 12:39

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coach",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("coach_name", models.CharField(max_length=256, verbose_name="教练名称")),
                ("phone", models.IntegerField(verbose_name="电话号码")),
                (
                    "tream_emblem",
                    models.ImageField(
                        default="default.jpg", upload_to="tream", verbose_name="球队队徽"
                    ),
                ),
                ("tream_name", models.CharField(max_length=256, verbose_name="球队名称")),
            ],
            options={"verbose_name_plural": "教练", "db_table": "Coach",},
        ),
        migrations.CreateModel(
            name="NewUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "roles",
                    models.IntegerField(
                        choices=[[0, "admin"], [1, "user"]],
                        default=1,
                        verbose_name="角色",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        default="default.jpg", upload_to="avatar", verbose_name="头像"
                    ),
                ),
                ("age", models.IntegerField(null=True, verbose_name="年龄")),
                ("phone", models.CharField(max_length=11, verbose_name="手机号")),
                (
                    "sex",
                    models.CharField(
                        choices=[["0", "女"], ["1", "男"]],
                        max_length=32,
                        null=True,
                        verbose_name="性别",
                    ),
                ),
                ("weight", models.FloatField(null=True, verbose_name="体重")),
                ("stature", models.FloatField(null=True, verbose_name="身高")),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ["0", "前锋"],
                            ["1", "左边锋"],
                            ["2", "右边锋"],
                            ["3", "前腰"],
                            ["4", "中前卫"],
                            ["5", "中后卫"],
                            ["6", "左后卫"],
                            ["7", "右后卫"],
                            ["8", "门将"],
                        ],
                        max_length=32,
                        null=True,
                        verbose_name="位置",
                    ),
                ),
                ("pass_football", models.FloatField(default=0, verbose_name="传球")),
                ("hotshot", models.FloatField(default=0, verbose_name="射门")),
                ("body", models.FloatField(default=0, verbose_name="身体")),
                ("defend", models.FloatField(default=0, verbose_name="防守")),
                ("speed", models.FloatField(default=0, verbose_name="速度")),
                ("control", models.FloatField(default=0, verbose_name="盘带")),
                ("score", models.FloatField(default=0, verbose_name="总评")),
                (
                    "football_tream",
                    models.CharField(max_length=64, null=True, verbose_name="球队"),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="创建时间"
                    ),
                ),
                (
                    "coa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.coach"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "NewUser",
                "abstract": False,
                "swappable": "AUTH_USER_MODEL",
            },
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("success", "success"),
                            ("info", "info"),
                            ("warning", "warning"),
                            ("error", "error"),
                        ],
                        default="info",
                        max_length=20,
                    ),
                ),
                ("unread", models.BooleanField(db_index=True, default=True)),
                ("actor_object_id", models.CharField(max_length=255)),
                ("verb", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "target_object_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "action_object_object_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("public", models.BooleanField(db_index=True, default=True)),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                ("emailed", models.BooleanField(db_index=True, default=False)),
                ("data", jsonfield.fields.JSONField(blank=True, null=True)),
                (
                    "action_object_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notify_action_object",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "actor_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notify_actor",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "target_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notify_target",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "通知",
                "ordering": ("-timestamp",),
                "abstract": False,
                "index_together": {("recipient", "unread")},
            },
        ),
    ]
