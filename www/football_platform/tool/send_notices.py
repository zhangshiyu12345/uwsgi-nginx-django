from notifications.signals import notify


class SendNotices():
    #actor:发件人
    #recipient:收件人
    #verb:动作
    def send(self,actor,recipient,verb,target=None,description=None):
        notify.send(sender=actor,recipient=recipient,verb=verb,target=target,description=description,level='danger')
    #获取未读列表
    def get_unread_list(self,user):
        return user.notifications.unread()




if __name__ == '__main__':
    notice = SendNotices()
    notice.send()
