from datetime import timedelta, datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .email import send_email_with_no_reply, compose_writing_task_email
import uuid


DEPARTMENTS = [
    ("TUT", "教学部"),
    ("CM", "行研部"),
    ("IT", "IT部"),
    ("HR", "人事部"),
    ("PR", "宣传部"),
    ("FIN", "财务部"),
    ("LAW", "法务部"),
    ("LIA", "外联部"),
    ("PRE", "主席团")
]

def getDeptName(code):
    global DEPARTMENTS
    for choice in DEPARTMENTS:
        if choice[0] == code:
            return choice[1]
    return "未知"

# Create your models here.
class Applicant(models.Model):
    global DEPARTMENTS
    
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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
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
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
        
    class Meta:
        verbose_name = "申请者"
        verbose_name_plural = "申请者"
        db_table = "申请人表"
        ordering = ["created_at"]
        
    def __str__(self):
        return self.name
    
class ApplicationStatus(models.Model):
    global DEPARTMENTS

    APPLICATION_STATUS = [
        ("NEW_APPLICATION", "新申请"),
        ("WRTIING_TASK_EMAIL_SENT", "笔试邮件已发送"),
        ("INTERVIEW_PENDING", "等待面试"),
        ("INTERVIEW_EMAIL_SENT", "面试邮件已发送"),
        ("PENDING", "面试结束, 待确认"),
        ("SEND_TO_OTHER_DEPT", "转去其他部门"),
        ("INTERNAL_ACCEPTED", "决定录取"),
        ("INTERNAL_REJECTED", "决定拒绝"),
        ("ACCEPTED", "已发送录取通知"),
        ("REJECTED", "已发送拒绝通知"),
        ("EXPIRED", "已过期"),
    ]
    
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f"writing_test/user_{instance.applicant.id}/{instance.handle_by}-{filename}"
    
    def calculate_ddl():
        ddl_datetime = datetime.now() + timedelta(days=7)
        return ddl_datetime.replace(hour=23, minute=59, second=59, microsecond=0)
    
    id = models.AutoField(primary_key=True)
    
    applicant = models.ForeignKey("Applicant", on_delete=models.CASCADE, related_name="applications", verbose_name="申请人", blank=False)
    
    status = models.CharField(max_length=25, choices=APPLICATION_STATUS, verbose_name="申请状态", default="NEW_APPLICATION")
    handle_by = models.CharField(max_length=3, choices=DEPARTMENTS, verbose_name="处理部门", blank=False)
        
    writing_task_ddl = models.DateTimeField(verbose_name="笔试截止时间", default=calculate_ddl, blank=False)
    writing_task_file = models.FileField(upload_to=user_directory_path,  verbose_name="笔试文件", blank=True, null=True, )
    writing_task_video_link = models.URLField(verbose_name="试讲视频链接", blank=True, null=True)
    
    interview_time = models.DateTimeField(verbose_name="面试时间", blank=True, null=True)
    interviewer = models.ForeignKey("Interviewer", on_delete=models.SET_NULL, verbose_name="主面试官", blank=True, null=True)
    
    writiing_task_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name="笔试总分", blank=True, null=True)
    interview_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name="面试总分", blank=True, null=True)

    writing_task_comment = models.TextField(verbose_name="笔试备注", blank=True, null=True)
    interview_comment = models.TextField(verbose_name="面试备注", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name = "申请状态"
        verbose_name_plural = "申请状态"
        db_table = "申请状态表"
        ordering = ["created_at"]
        unique_together = ["applicant", "handle_by"]
    
    def __str__(self):
        return f"{self.applicant.name} - {getDeptName(self.handle_by)}"
    
    def send_writing_task_email(self):
        if self.status != "NEW_APPLICATION":
            return False
        res = send_email_with_no_reply(self.applicant.email, "SAGA星光·第五期 -- 笔试邀请",
                                 compose_writing_task_email(self.applicant.id, self.applicant.name,
                                                            self.handle_by, self.writing_task_ddl))
        if res:
            self.status = "WRTIING_TASK_EMAIL_SENT"
            self.save()
            return True
        return False

    def send_interview_email(self):
        if self.status != "INTERVIEW_PENDING":
            return False
        print(f"send email to interview: {self.applicant.email}")
        return True
    
    def send_decision_email(self):
        if self.status not in ["INTERNAL_ACCEPTED", "INTERNAL_REJECTED"]:
            return False
        if self.status == "INTERNAL_ACCEPTED":
            print(f"send email to accept: {self.applicant.email}")
        else:
            print(f"send email to reject: {self.applicant.email}")
        return True
    
class Interviewer(models.Model):
    global DEPARTMENTS
    
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=10, verbose_name="姓名", blank=False)
    department = models.CharField(max_length=3, choices=DEPARTMENTS, verbose_name="部门", blank=False)
    meeting_link = models.URLField(verbose_name="面试链接", blank=False)
    
    class Meta:
        verbose_name = "面试官"
        verbose_name_plural = "面试官"
        db_table = "面试官表"
        ordering = ["department"]
    
    def __str__(self):
        return f"{self.name} - {getDeptName(self.department)}"