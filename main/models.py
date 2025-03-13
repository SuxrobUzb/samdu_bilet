from django.db import models
import os





class SamDUkf(models.Model):
    """
    Ushbu model akademik yil, semestr, fan, bosqich va mutaxassislik bo'yicha
    ma'lumotlarni saqlash uchun ishlatiladi.
    """
    uquv_yili = models.ForeignKey(
        "Uquv_yili", 
        on_delete=models.CASCADE,
        verbose_name="O'quv yili"  # verbose_name qo'shildi
    )
    semestr = models.ForeignKey(
        "Semestr", 
        on_delete=models.CASCADE,
        verbose_name="Semestr"
    )
    fan = models.ForeignKey(
        "Fan", 
        on_delete=models.CASCADE,
        verbose_name="Fan"
    )
    bosqich = models.ForeignKey(
        "Bosqich", 
        on_delete=models.CASCADE,
        verbose_name="Bosqich"
    )
    talim_yunalishi = models.ForeignKey(
        "Talim_yunalishi", 
        on_delete=models.CASCADE,
        verbose_name="Ta'lim yo'nalishi"
    )
    file = models.FileField(
        upload_to='documents/',
        null=True, 
        blank=True,
        help_text="Yuklangan fayl",
        verbose_name="Fayl"  # verbose_name qo'shildi
    )
    biletlar_soni = models.IntegerField(
        default=1,
        help_text="nechta bilet kerakligini kiriting?",
        verbose_name="Biletlar soni"
    )
    oson_savol = models.IntegerField(
        default=1,
        help_text="oson savollar",
        verbose_name="Oson savollar"
    )
    urtacha_savol = models.IntegerField(
        default=1,
        help_text="urtacha darajali savollar",
        verbose_name="O'rtacha savollar"
    )
    murakkab1 = models.IntegerField(
        default=1,
        help_text="murakkab1 darajaga mansub savollar",
        verbose_name="Murakkab 1 savollar"
    )
    murakkab2 = models.IntegerField(
        default=1,
        help_text="murakkab2 darajaga mansub savollar",
        verbose_name="Murakkab 2 savollar"
    )
    qiyin_savol = models.IntegerField(
        default=1,
        help_text="eng qiyin savollar tuplami",
        verbose_name="Qiyin savollar"
    )

    def __str__(self):
        return f"{self.fan} ({self.uquv_yili})"

    class Meta:
        verbose_name = "SamDU KF Ma'lumoti"
        verbose_name_plural = "SamDU KF Ma'lumotlari"





class Uquv_yili(models.Model):
    """
    Ushbu model o'quv yili bo'yicha ma'lumotlarni saqlash uchun ishlatiladi.
    """
    uquv_yili = models.CharField(max_length=20, verbose_name="O'quv yili")

    def __str__(self):
        return f"{self.uquv_yili}"
    
class Bosqich(models.Model):
    """
    Ushbu model bosqich raqamini saqlash uchun ishlatiladi.
    """
    bosqich = models.IntegerField(default=0, verbose_name="Bosqich")
    
    def __str__(self):
        return f"{self.bosqich}"
    

class Talim_yunalishi(models.Model):
    """
    Ushbu model mutaxassislik nomini saqlash uchun ishlatiladi.
    """
    talim_yunalishi = models.CharField(max_length=200, verbose_name="Ta'lim yo'nalishi" ) # verbose_name qo'shildi)
    
    def __str__(self):
        return f"{self.talim_yunalishi.capitalize()}"
    
class Semestr(models.Model):
    """
    Ushbu model semestr nomini saqlash uchun ishlatiladi.
    """
    semestr = models.CharField(max_length=10, verbose_name="Semestr" ) # verbose_name qo'shildi
    
    def __str__(self):
        return f"{self.semestr}"
    
class Fan(models.Model):
    """
    Ushbu model fan nomini saqlash uchun ishlatiladi.
    """
    fan = models.CharField(max_length=200, verbose_name="Fan" ) # verbose_name qo'shildi)
    
    def __str__(self):
        return f"{self.fan.capitalize()}"
    




def get_upload_path(instance, filename):
    # Har bir samdukf uchun statik fayl nomi
    return os.path.join('biletlar', f"merged_tickets_{instance.samdukf.id}.pdf")

class SamDUkfDoc(models.Model):
    samdukf = models.OneToOneField('SamDUkf', on_delete=models.SET_NULL, null=True, blank=True, related_name='samdukfdoc', verbose_name="Fayl")
    file = models.FileField(upload_to='documents/', help_text="tayyor biletlar", verbose_name="Fayl")

    def save(self, *args, **kwargs):
        # Eski faylni topish va o'chirish
        if self.pk:
            try:
                old_instance = SamDUkfDoc.objects.get(pk=self.pk)
                if old_instance.file and os.path.isfile(old_instance.file.path):
                    print(f"Attempting to delete old file: {old_instance.file.path}")
                    try:
                        os.remove(old_instance.file.path)
                        print(f"Successfully deleted old file: {old_instance.file.path}")
                    except Exception as e:
                        print(f"Failed to delete old file: {str(e)}")
            except SamDUkfDoc.DoesNotExist:
                pass

        # Yangi faylni saqlash
        super().save(*args, **kwargs)

        if self.file:
            print(f"Saved (overwritten) file: {self.file.path}")
        else:
            print("No file associated with this instance after save.")

    def delete(self, *args, **kwargs):
        # Faylni o'chirish
        if self.file and os.path.isfile(self.file.path):
            print(f"Attempting to delete file from filesystem: {self.file.path}")
            try:
                os.remove(self.file.path)
                print(f"Successfully deleted file: {self.file.path}")
            except Exception as e:
                print(f"Failed to delete file: {str(e)}")

        # Bazadan o'chirish
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Tayyor biletlar - {self.samdukf.id if self.samdukf else 'No SamDUkf'}"





































        # ----------------------------------------------------------------------


