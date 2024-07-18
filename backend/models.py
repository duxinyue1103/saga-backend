from django.db import models

# Create your models here.
class Applicant(models.Model):
    
    YEAR_IN_SCHOOL_CHOICES = [
        ("UG1", "大一"),
        ("UG2", "大二"),
        ("UG3", "大三"),
        ("UG4", "大四"),
        ("UGGRAD", "本科毕业"),
        ("PG", "硕/博士生"),
        ("PGGRAD", "硕/博士毕业"),
        ("OTHER", "其他"),
    ]
    
    DEPARTMENTS = [
        ("TUT", "教学部"),
        ("CM", "行研部"),
        ("IT", "IT部"),
        ("HR", "人事部"),
        ("PR", "宣传部"),
        ("FIN", "财务部"),
        ("LAW", "法务部"),
        ("LIA", "外联部"),
    ]
    
    SUBJECTS = [
        ("MATH", "数学"),
        ("CHI", "语文"),
        ("ENG", "英语"),
    ]
    
    SEX = [
        ("M", "男"),
        ("F", "女"),
        ("O", "其他"),
    ]
    
    APPLICATION_STATUS = [
        ("INTERVIEW_PENDING", "等待面试"),
        ("PENDING", "待确认"),
        ("INTERNAL_ACCEPTED", "内部决定录取"),
        ("INTERNAL_REJECTED", "内部决定拒绝"),
        ("ACCEPTED", "已发送录取通知"),
        ("REJECTED", "已发送拒绝通知"),
        ("NEW_APPLICATION", "新申请"),
        ("WRITTEN_TEST_REVEIVED", "收到笔试"),
        ("EXPIRED", "已过期"),
    ]
    
    
    name = models.CharField(max_length=10, verbose_name="姓名", blank=False)
    email = models.EmailField(max_length=30, verbose_name="邮箱", blank=False)
    phone = models.CharField(max_length=11, verbose_name="手机号码(+86)", blank=False)
    school = models.CharField(max_length=30, verbose_name="就读院校", blank=False)
    major = models.CharField(max_length=30, verbose_name="专业", blank=False)
    grade = models.CharField(max_length=6, choices=YEAR_IN_SCHOOL_CHOICES, verbose_name="年级", blank=False)
    sex = models.CharField(max_length=1, choices=SEX, verbose_name="性别", default="O")
    wechat = models.CharField(max_length=30, verbose_name="微信号", blank=False)
    first_choice = models.CharField(max_length=3, choices=DEPARTMENTS, verbose_name="第一志愿", blank=False)
    second_choice = models.CharField(max_length=3, choices=DEPARTMENTS, verbose_name="第二志愿", blank=True, null=True)
    third_choice = models.CharField(max_length=3, choices=DEPARTMENTS, verbose_name="第三志愿", blank=True, null=True)
    preferred_subject = models.CharField(max_length=4, choices=SUBJECTS, verbose_name="偏好科目", blank=True, null=True)
    self_intro = models.TextField(verbose_name="简述", blank=False)
    disposable_time = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=False, verbose_name="每周可投入小时")
    src = models.CharField(max_length=30, verbose_name="来源", blank=True, null=True)
    
    application_status = models.CharField(max_length=25, choices=APPLICATION_STATUS, verbose_name="申请状态", blank=True, default="NEW_APPLICATION")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = "申请者"
        verbose_name_plural = "申请者"
        db_table = "申请人表"
        ordering = ["created_at"]
        
    def __getDeptName(self):
        for choice in self.DEPARTMENTS:
            if choice[0] == self.first_choice:
                return choice[1]
        return "未知"
    
    def __getApplicantStatus(self):
        for choice in self.APPLICATION_STATUS:
            if choice[0] == self.application_status:
                return choice[1]
        return "未知"
        
    def __str__(self):
        return f"{self.name} - {self.__getDeptName()} - {self.__getApplicantStatus()}"
    