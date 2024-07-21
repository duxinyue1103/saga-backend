import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
dept_to_file_url = {
    "TUT": "http://example.com/TUT_exam",
    "CM": "http://example.com/CM_exam",
    "IT": "http://example.com/IT_exam",
    "HR": "http://example.com/HR_exam",
    "PR": "http://example.com/PR_exam",
    "FIN": "http://example.com/FIN_exam",
    "LAW": "http://example.com/LAW_exam",
    "LIA": "http://example.com/LIA_exam",
}

def compose_writing_task_email(id, name, dept, ddl):
    file_url = dept_to_file_url.get(dept, "http://example.com/default_exam")
    content = f"""
  <html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Simple Transactional Email</title>
    <style media="all" type="text/css">
    /* -------------------------------------
    GLOBAL RESETS
------------------------------------- */
    
    body {{
      font-family: Helvetica, sans-serif;
      -webkit-font-smoothing: antialiased;
      font-size: 16px;
      line-height: 1.3;
      -ms-text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
      
    }}
    
    table {{
      border-collapse: separate;
      /* mso-table-lspace: 0pt;
      mso-table-rspace: 0pt; */
      width: 100%;
    }}
    
    table td {{
      font-family: Helvetica, sans-serif;
      font-size: 16px;
      vertical-align: top;
    }}
    /* -------------------------------------
    BODY & CONTAINER
------------------------------------- */
    
    body {{
      background-color:rgb(255,189,89);
      margin: 0;
      padding: 0;
    }}

    .body {{ 
      width: 100%;
    }}
    .signature-thin{{
      margin-top: 3em;
      line-height: 0.4;
      font-size: 12px;
    }}
    .signature-plus {{
      margin-top: 2em;
      line-height: 0.4;
      font-style: italic;
    }}
    .highlight {{
      font-weight: bold;
      color: #dcac0f;
    }}
    .highlight-thin {{
      color: #dcac0f;
      font-style:oblique;
    }}
    .des-post{{
        font-size: 14px;
    }} 
    .container {{
      margin: 0 auto !important;
      max-width: 600px;
      padding: 0;
      padding-top: 24px;
      width: 600px;
    }}
    
    .content {{
      box-sizing: border-box;
      display: block;
      margin: 0 auto;
      max-width: 600px;
      padding: 0;
    }}
    /* -------------------------------------
    HEADER, FOOTER, MAIN
------------------------------------- */
    
    .main {{
      background: #ffffff;
      border: 1px solid #eaebed;
      border-radius: 16px;
      width: 100%;
    }}
    
    .wrapper {{
      box-sizing: border-box;
      padding: 24px;
    }}
    
    .footer {{
      clear: both;
      padding-top: 24px;
      padding-bottom: 5%;
      text-align: center;
      width: 100%;
    }}
    
    .footer td,
    .footer p,
    .footer span,
    .footer a {{
      color: #d37d37;
      font-size: 16px;
      text-align: center;
    }}
    /* -------------------------------------
    TYPOGRAPHY
------------------------------------- */
    
    p {{
      font-family: Helvetica, sans-serif;
      font-size: 16px;
      font-weight: normal;
      margin: 0;
      margin-bottom: 16px;
    }}
    a:link{{		/*默认状态*/
      color: #dcac0f;
    }}
    a:visited{{	/*浏览过的*/
      color:rgb(255,167,27);
    }}
    a:hover{{	/*悬浮状态*/
      color:rgb(255,195,33);
    }}
    a:active{{	/*激活过的*/
      color:rgb(255,141,27);
    }}
    .namestyle{{
      font-style: italic;
      font-weight: bold;
      color: #dcac0f;
    }}
    /* -
    OTHER STYLES THAT MIGHT BE USEFUL
------------------------------------- */
    .preheader {{
      color: transparent;
      display: none;
      height: 0;
      max-height: 0;
      max-width: 0;
      opacity: 0;
      overflow: hidden;
      /* mso-hide: all; */
      visibility: hidden;
      width: 0;
    }}
    
    .powered-by a {{
      text-decoration: none;
    }}
    
    /* -------------------------------------
    RESPONSIVE AND MOBILE FRIENDLY STYLES
------------------------------------- */
    
    @media only screen and (max-width: 640px) {{
      .main p,
      .main td,
      .main span {{
        font-size: 16px !important;
      }}
      .wrapper {{
        padding: 8px !important;
      }}
      .content {{
        padding: 0 !important;
      }}
      .container {{
        padding: 0 !important;
        padding-top: 8px !important;
        width: 100% !important;
      }}
      .main {{
        border-left-width: 0 !important;
        border-radius: 0 !important;
        border-right-width: 0 !important;
      }}
    }}
    /* -------------------------------------
    PRESERVE THESE STYLES IN THE HEAD
------------------------------------- */
    
    @media all {{
      .ExternalClass {{
        width: 100%;
      }}
      .ExternalClass,
      .ExternalClass p,
      .ExternalClass span,
      .ExternalClass font,
      .ExternalClass td,
      .ExternalClass div {{
        line-height: 100%;
      }}
      .apple-link a {{
        color: inherit !important;
        font-family: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        text-decoration: none !important;
      }}
      #MessageViewBody a {{
        color: inherit;
        text-decoration: none;
        font-size: inherit;
        font-family: inherit;
        font-weight: inherit;
        line-height: inherit;
      }}
    }}
    /* picture */

   .pic-top{{
     display: flex;
     flex-direction: column;
     text-align: center;
     justify-content: center;
     align-items: center;
     width: 100%;
   }}
   .pic-top img {{
      width: 100%;
      height: auto;
    }}
   
    </style>
  </head>
  <body>
    <div class="pic-top">
      <img src="http://saga-xingguang.com/static/public/imgs/writing-task-email-banner.jpg" alt="">
    </div>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
      <tr>
        <td>&nbsp;</td>
        <td class="container">
          <div class="content">

            <!-- START CENTERED WHITE CONTAINER -->
            <span class="preheader">SAGA星光·第五期 - 笔试邀请</span>
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper">
                  <p>亲爱的{name}同学,</p>
                  <p>您好!</p>
                  <p>感谢您参加志行会SAGA星光线上课堂项目<span class="highlight">{code_to_dept[dept]}</span>的招募。我们诚挚地邀请您参加此次招募的第一轮环节——笔试环节。(请仔细查看笔试考核相关文件)</p>
                  <p>您可以从下方的链接中下载笔试文件，并在原文档上进行编辑。如您所申请的组别有录制试讲要求，请您仔细查看附件相关内容。<br>请您在收到笔试考核的<span class="highlight">七天内({ddl} 前)</span>将您的所有笔试文件全部放至一个PDF文件内并上传至下方提供的提交链接中，若逾期提交，我们将视为主动放弃。</p>
                  
                  <p>您的文件下载链接是: <a href="{file_url}">下载笔试题目</a>    ，您的文件提交链接是:  <a href="http://www.saga-xingguang.com/appreciation/volunteers/upload-writing-task?id={id}">提交笔试文件</a></p>
        
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" >
                    <tbody>
                      <tr>
                        <td align="left">
                          <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            <tbody>                             
                            </tbody>           
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <p>如果您对以上安排有任何疑问或要求，请您尽快通过邮箱与我们联络，我们将与您做进一步交流。
                  <br>
                  <span class="des-post">技术支持邮箱：</span><span class="highlight-thin">support@saga-xingguang.com</span>
                  <br>
                  <span class="des-post">人事部邮箱：</span><span class="highlight-thin">human-resources@saga-xingguang.com</span>
                  </p>
                  <div class="signature-thin">
                    <p>顺颂，</p>
                    <p>夏祺</p>
                  </div>
                  <div class="signature-thin">
                    <p>志行会SAGA星光项目组·{code_to_dept[dept]}敬上</p>
                    <p>---SAGA星光团队 </p>
                  </div>
                  
                </td>
              </tr>

              <!-- END MAIN CONTENT AREA -->
              </table>

            <!-- START FOOTER -->
            <div class="footer">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                <tr>
                  <td class="content-block">
                    <span class="apple-link">微信公众号：星光SAGA</span>
                    <br>
                    
                  </td>
                </tr>
                <tr>
                  <!-- <td class="content-block powered-by">
                    Powered by <a href="http://htmlemail.io">HTMLemail.io</a>
                  </td> -->
                </tr>
              </table>
            </div>

            <!-- END FOOTER -->
            
<!-- END CENTERED WHITE CONTAINER --></div>
        </td>
        <td>&nbsp;</td>
      </tr>
    </table>
    
  </body>
</html>


"""
    return content


def send_email_with_no_reply(to, subject, content) -> bool:
    try:
        sender = "no-reply@saga-xingguang.com"
        server = smtplib.SMTP('smtp.feishu.cn', 587)
        server.starttls()
        server.login(sender, "PASSWORD_HERE")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to
        msg["Reply-To"] = "support@saga-xingguang.com"

        html_part = MIMEText(content, "html", "utf-8")
        msg.attach(html_part)

        server.sendmail(sender, to, msg.as_string())
        server.quit()
        return True
        
    except Exception as e:
        print(e)
        return False
      