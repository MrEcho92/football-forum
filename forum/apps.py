from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    def ready(self):
        import forum.signals



         #comment signals to execute affer save function
    #     post_save.connect(user_comment_post, sender=Comment) #receviver (function), sender
    #     post_delete.connect(user_del_comment_post, sender=Comment)
