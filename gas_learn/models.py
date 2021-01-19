from django.db import models

"""
Models this application using
""" 

class BlockInfo(models.Model): 
    """
    block info of messages
    """
    epoch = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    block_count = models.IntegerField()
    basefee = models.BigIntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'blockinfo'
        managed = True
        ordering = ["epoch"]
        verbose_name = 'blockinfo'
        verbose_name_plural = 'blockinfos'

class BlockCateInfo(models.Model):
    """
    category info the different types of message info
    """
    epoch = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    cate_code = models.IntegerField()
    count = models.IntegerField()
    gas_limit_avg = models.BigIntegerField(null=True, blank=True)
    gas_limit_total = models.BigIntegerField(null=True, blank=True)
    gas_cap_avg = models.BigIntegerField(null=True, blank=True)
    gas_cap_total = models.BigIntegerField(null=True, blank=True)
    gas_premium_avg = models.BigIntegerField(null=True, blank=True)
    gas_premium_total = models.BigIntegerField(null=True, blank=True)
    value = models.BigIntegerField(null=True, blank=True)
    
    foreign = models.ForeignKey(BlockInfo, related_name="cates", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        ordering = ["created"]
    

class MpoolInfo(models.Model):
    """
    mpool info of messages
    """
    created = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'mpoolinfo'
        managed = True
        ordering = ["epoch"]
        verbose_name = 'mpoolinfo'
        verbose_name_plural = 'mpoolinfos'


class MpoolCateInfo(models.Model):
    """
    category info the different types of message info
    """
    created = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField()
    cate_code = models.IntegerField()
    count = models.IntegerField()
    gas_limit_avg = models.BigIntegerField(null=True, blank=True)
    gas_limit_total = models.BigIntegerField(null=True, blank=True)
    gas_cap_avg = models.BigIntegerField(null=True, blank=True)
    gas_cap_total = models.BigIntegerField(null=True, blank=True)
    gas_premium_avg = models.BigIntegerField(null=True, blank=True)
    gas_premium_total = models.BigIntegerField(null=True, blank=True)
    value = models.BigIntegerField(null=True, blank=True)

    foreign = models.ForeignKey(MpoolInfo, related_name="cates", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        ordering = ["created"]






    


