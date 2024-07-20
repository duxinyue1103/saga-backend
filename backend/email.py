import smtplib
from email.mime.text import MIMEText
code_to_dept = {
    "TUT": "教学部",
    "CM": "行研部",
    "IT": "IT部",
    "HR": "人事部",
    "PR": "宣传部",
    "FIN": "财务部",
    "LAW": "法务部",
    "LIA": "外联部",
}


def compose_email(id, name, dept, date):
    content = f"""
申请人{name},
你好!

\t我们已经收到了你对 SAGA星光·第五期: {code_to_dept[dept]} 的申请. 

请你在 {date} 的7天内前往 连接 下载笔试文件并完成.

上传链接: http://www.saga-xingguang.com/appreciation/volunteers/upload-writing-test?id={id}

\t如果你有任何问题, 请联系我们.

祝好,
SAGA星光

"""
    return content


def send_email(to, subject, content) -> bool:
    try:
        sender = "no-reply@saga-xingguang.com"
        server = smtplib.SMTP('smtp.feishu.cn', 587)
        server.starttls()
        server.login(sender, "PASSWORD")
        text = MIMEText(content, "plain", "utf-8")
        text["Subject"] = subject
        text["From"] = sender
        text["To"] = to
        text["Reply-To"] = "support@saga-xingguang.com"
        
        status = server.sendmail(sender, to, text.as_string())
        server.quit()
        if not status:
            return True
        else:
            return False
        
    except Exception as e:
        print(e)
        return False