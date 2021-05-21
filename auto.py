#-*-coding:utf-8-*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import string
import traceback
import sys

import urllib 
import urllib2 
import requests
import re 
import os

import random

runHourMin=9
runHourMax=22
loginUserName=""
loginPassWord=""
classListUrl=""

def checkNowTime():
    hour=time.localtime().tm_hour
    nowTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if(hour>runHourMax or hour<runHourMin):
        print ("%s 不在运行时间(%s:00-%s:00)范围内。退出" %(nowTime,runHourMin,runHourMax)).encode("gb18030")
        sys.exit();
    else:
        print ("%s 仅在%s点 - %s点间运行，超过时间自动退出" %(nowTime,runHourMin,runHourMax)).encode("gb18030")

def randomsleep():
    time.sleep(random.randint(0,5)*10);

stepSleepSecond=10

# 等待观看时间是否完成的函数
def checktime():
    #检查方式1 按上方的学习时间
    try:
        count=0
        #循环等待符合时间要求
        while(True):
            #计算时间
            #观看时长不少于xx分钟
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//span[@class='cl-head-tip']/time[1]"))
            )
            mintime=int(element.text)
            #已学习xx分钟
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//span[@class='cl-head-tip']/time[2]"))
            )
            nowtime=int(element.text)
            print ("需观看%d 分钟，已学习 %d 分钟 。" %(mintime,nowtime)).encode("gb18030")
            if(mintime-nowtime-count)>0 :
                time.sleep(60)
                count=count+1
            else:
                break
        print "已符合学习时间要求。".encode("gb18030")
        #按时间判断经常会学不完，改成按图标变化判断
        count=0
        while(True):
            time.sleep(60)
            count=count+1
            if(count>5):
                print "在符合时间要求后已经多等了5分钟仍然没有学完。跳出".encode("gb18030")
                break
            #判断该章节是否已经学完（检查是否有对钩图标）
            try:
                icon=sub.get_attribute("class")
                if ("done" in icon) :
                    print "学完了".encode("gb18030")
                    break
            except:
                pass
        return;
    except Exception, e:
        errmsg=traceback.format_exc()
        print '方式1检查异常：，错误信息: '.encode("gb18030"),errmsg.encode("gb18030")
    
    #检查方式2 按下方的视频播放时间检查
    currenttime = WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//span[@class='current-time']"))
    )

    duration = WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//span[@class='duration']"))
    )
    
    count=0
    #循环等待符合时间要求
    time.sleep(stepSleepSecond)
    while(currenttime.text!=duration.text):
        print ("视频播放中"+currenttime.text+"/"+duration+"\r").encode("gb18030"),
        time.sleep(1)
        count=count+1
    print "视频已播放完。".encode("gb18030")
    #按时间判断经常会学不完，改成按图标变化判断
    count=0
    while(True):
        time.sleep(5)
        count=count+1
        if(count>10):
            print "在符合时间要求后已经多等了5分钟仍然没有学完。跳出".encode("gb18030")
            break
        #判断该章节是否已经学完（检查是否有对钩图标）
        try:
            element=sub.find_element(By.XPATH,"./../span[2]");
            icon=element.get_attribute("class")
            if ("finish-tig" in icon) :
                print "学完了".encode("gb18030")
                break
        except:
            pass
    return;

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')   

checkNowTime();



if classListUrl=="":
    print "输入课程列表url".encode('gb18030') 
    while(True):
        line = sys.stdin.readline().strip()
        if line == "" :
            pass;
        else:
            classListUrl=line
            break

print "是否显示chrome，默认显示，输入n不显示".encode('gb18030') 
show_chrome=True
line = sys.stdin.readline().strip()
if line == "n" or line== "N":
    show_chrome=False
else:
    pass

if loginPassWord=="" :
    print "输入用于登录的用户名".encode('gb18030') 
    loginUserName = sys.stdin.readline().strip()
    print "输入密码".encode('gb18030') 
    loginPassWord = sys.stdin.readline().strip()
    
download_mode=False
##是否下载mp4文件
#print "是否下载MP4视频，y下载n不下，默认n".encode('gb18030') 
#print "只能下载mp4的课，并且要没有课后答题，否则会报错".encode('gb18030') 
#line = sys.stdin.readline().strip()
#if line == "Y" or line== "y":
#    download_mode=True
#else:
#    pass

print "输入数字，跳过一些课程，从第n个课开始学n>=1，默认从头学".encode('gb18030') 
line = sys.stdin.readline().strip()
kc_skip=0
try:
    kc_skip=int(line)
except:
    print "从头学".encode('gb18030') 
    pass

options = webdriver.ChromeOptions()
#options.add_argument('lang=zh_CN.UTF-8')
options.add_argument("--user-data-dir=./ChromeUserData/aaa")
options.add_argument("start-maximized"); # open Browser in maximized mode
options.add_argument("disable-infobars"); # disabling infobars
#options.add_argument("--disable-extensions"); # disabling extensions
#options.add_argument("--disable-gpu"); # applicable to windows os only
options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
options.add_argument("--no-sandbox"); # Bypass OS security model
options.add_argument("--remote-debugging-port=9222")  # 解决报错 WebDriverException: Message: unknown error: DevToolsActivePort file doesn't exist
if show_chrome==False :
    options.add_argument("--headless") ##不打开chrome窗口，防止浏览器窗口切换到前台
options.add_argument('--no-proxy-server')  #使用headless 访问网址特别慢的问题
options.add_argument("--proxy-server='direct://'");
options.add_argument("--proxy-bypass-list=*");

options.add_argument('--ignore-certificate-errors')   #处理报错问题  ERROR:ssl_client_socket_impl.cc(947)] handshake failed; returned -1, SSL error code 1, net_error -101
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

browser = webdriver.Chrome(chrome_options = options)

time.sleep(5)
browser.get(classListUrl)
#browser.get("https://eln.so/u0rNE01zS")
print "访问网址".encode('gb18030') 
time.sleep(stepSleepSecond)

#如果打开了登录页面，则自动登录
try:
    element = WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//span[contains(@class,'psd-login')]"))
    )
    print "登录页面".encode('gb18030')
    element.click()
    time.sleep(stepSleepSecond)
    print "登录".encode('gb18030')
    username = WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//input[@id='loginName']"))
    )
    username.clear()
    username.send_keys(loginUserName)
    password = WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//input[@id='swInput']"))
    )
    password.clear()
    password.send_keys(loginPassWord)
    time.sleep(2)
    loginbtn= WebDriverWait(browser, stepSleepSecond).until(
        EC.presence_of_element_located((By.XPATH,"//button[contains(@class,'login-btn')]"))
    )
    loginbtn.click()
    try:
        surebtn= WebDriverWait(browser, stepSleepSecond).until(
            EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'sure')]/button"))
        )
        surebtn.click()
    except:
        pass
    time.sleep(stepSleepSecond)
    
except Exception, err:
    errmsg=traceback.format_exc()
    print '登录异常,错误: '.encode("gb18030"),errmsg.encode("gb18030")

courseListWindowHandle = browser.current_window_handle

#确认课程组页面
while True:
    # 
    # 获取页面的 title和handle信息
    courseListWindowHandle = browser.current_window_handle
    courseListTitle = browser.title
    try:

        #获取课程组的名字
        element = WebDriverWait(browser, stepSleepSecond).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='nc-subject-summary']"))
        )
        cltitle=element.text
    except:
        print "没有找到课程列表，在打开的浏览器中手工登录，并进入课程列表页面\n".encode('gb18030')
        print "按回车键继续".encode('gb18030')
        line = sys.stdin.readline().strip()
        
        #browser.get(classListUrl)
        
        continue
        
    #显示找到的课程列表，确认继续
    print "当前页面课程列表为:".encode('gb18030') , cltitle.encode('gb18030')
    print "输入Y开始学习，输入其他重新检查课程列表".encode('gb18030')
    line = sys.stdin.readline().strip()
    if line == "Y" or line== "y":
        break
    else:
        pass



# 获取页面的 title和handle信息
courseListWindowHandle = browser.current_window_handle
courseListTitle = browser.title

#获取课程列表
kclist = WebDriverWait(browser, stepSleepSecond).until(
    EC.presence_of_all_elements_located((By.XPATH,"//li/a[@data-id]"))
)


kc_no=0
kc_name=""
for kc in kclist:
    #遍历课程列表
    kc_no+=1
    if kc_no<=kc_skip:
        continue
    try:
        browser.switch_to_window(courseListWindowHandle)
        time.sleep(stepSleepSecond)

        kc_name=kc.text
        print "开始学习课程：".encode('gb18030'),kc_name.encode('gb18030')
        #点击课程，进入课程页面
        kc.click()
        time.sleep(stepSleepSecond)

        # 遍历找新窗口，切换到新打开的课程视频窗口
        # 拿到所有的窗口
        allHandles = browser.window_handles
        #print(f"3. allHandles = {allHandles}")
        routeWindowHandle = 0
        routeTitle = 'None'
        for handle in allHandles:
            if handle != courseListWindowHandle:
                browser.switch_to_window(handle)
                routeWindowHandle = browser.current_window_handle
                routeTitle = browser.title
                break

        ### 检查学习进度，如果是已完成则跳出
        time.sleep(stepSleepSecond)
        element = WebDriverWait(browser, stepSleepSecond).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='cd-details-msg']"))
        )
        cddetailsmsg=element.text
        if (string.find(cddetailsmsg,"已完成")!=-1 or string.find(cddetailsmsg,"100%")!=-1 or string.find(cddetailsmsg,"学习进度： 课后测试")!=-1) and download_mode==False:
            print cddetailsmsg.encode('gb18030')  ,"\n"
            print "课程状态不需要学习,或需要手动执行后续步骤，跳过\n".encode('gb18030')
            browser.close()
            continue
        else:
            pass

        #选课
        try:
            time.sleep(stepSleepSecond)
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.ID, "goStudyBtn"))
            )
            element.click()
        except:
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.ID, "chooseCourse"))
            )
            element.click()
            time.sleep(stepSleepSecond)
            try:
                #选课有时要确认如果找到确认按钮则点，找不到则执行下一步
                element = WebDriverWait(browser, stepSleepSecond).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "layui-layer-btn0"))
                )
                element.click()    
                time.sleep(stepSleepSecond)
            except:
                pass
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.ID, "goStudyBtn"))
            )
            element.click()
        #进入播放页面
        try:
            time.sleep(stepSleepSecond)
            #进入iframe
            try:
                browser.switch_to.frame(browser.find_element_by_id("aliPlayerFrame"))
            except:
                pass
            #判断是否有章节列表
            #查找章节列表 ，如果报错找不到，可能是学完了，直接进入了评分界面
            headListCount = 0
            try:
                headlist=WebDriverWait(browser, stepSleepSecond).until(
                    EC.presence_of_all_elements_located((By.XPATH,"//div[@class='section']/li"))
                )
                headListCount=len(headlist)
            except:
                pass
                
            if headListCount==0:
                print ("没有章节列表的课程，直接等待时间学完跳出".encode("gb18030"))
                checktime()
            else:
            
                #查找章节列表 ，如果报错找不到，可能是学完了，直接进入了评分界面
                sublist = WebDriverWait(browser, stepSleepSecond).until(
                    EC.presence_of_all_elements_located((By.XPATH,"//div[@class='section']/li/div[contains(@class,'first-line')]/span[1]"))
                )
                #循环章节
                sub_no=0
                sub_name=""
                for sub in sublist:
                    checkNowTime();
                    
                    time.sleep(stepSleepSecond)
                    
                    sub_no+=1
                    sub_name=sub.text
                    print "章节：".encode('gb18030'),sub_name.encode('gb18030')

                    #判断该章节是否已经学完（检查是否有对钩图标）
                    try:
                        element=sub.find_element(By.XPATH,"./../span[2]");
                        print element.get_attribute('innerHTML')
                        icon=element.get_attribute("class")
                        if ("finish-tig" in icon) :
                            print "已学完".encode("gb18030")
                            continue
                    except Exception, err:
                        errmsg=traceback.format_exc()
                        print '没有获取到章节学习状态,可能还没有学: '.encode("gb18030"),errmsg.encode("gb18030")
                        #pass

                    sub.click()
                    time.sleep(stepSleepSecond)

                    #切换2倍速
                    try:
                        rate_components = WebDriverWait(browser, stepSleepSecond).until(
                            EC.presence_of_element_located((By.XPATH,"//div[@class='rate-components']"))
                        )
                        time.sleep(stepSleepSecond)
                        element=rate_components.find_element(By.XPATH,"./div[@class='current-rate']");
                        element.click()
                        time.sleep(stepSleepSecond)
                        element=rate_components.find_element(By.XPATH,"./ul/li[@data-rate='2.0']");
                        element.click()
                    except Exception, err:
                        errmsg=traceback.format_exc()
                        print '切换2倍速错误: '.encode("gb18030"),errmsg.encode("gb18030")
                        #pass
                    
                    #下载视频
                    #获取视频链接
                    if download_mode==True:
                        try:
                            element = WebDriverWait(browser, stepSleepSecond).until(
                                EC.presence_of_element_located((By.XPATH,"//embed[1]"))
                            )
                            mp4link=urllib.unquote(element.get_attribute("flashvars").split("&")[0].split("=")[1])
                            file_ext=re.search(r'(\.[^.\\/:*?"<>]+)$', mp4link).group(1)
                            filename="%02d-%s-%02d-%s%s" % (kc_no, kc_name,sub_no,sub_name,file_ext)
                            if not os.path.exists(filename):
                                print ("下载 %s" %(filename)).encode("gb18030")
                                urllib.urlretrieve(mp4link, filename)
                        except Exception, e:
                            print 'str(Exception):\t', str(Exception).encode("gb18030")
                            print 'str(e):\t\t', str(e).encode("gb18030")
                            print 'repr(e):\t', repr(e).encode("gb18030")
                            print 'e.message:\t', e.message.encode("gb18030")
                            print 'traceback.print_exc():'; traceback.print_exc().encode("gb18030")
                            print 'traceback.format_exc():\n%s' % traceback.format_exc().encode("gb18030")
                        #只下视频，下完就退
                        continue

                    #判断该章节是否已经学完（检查是否有对钩图标）
                    try:
                        element=sub.find_element(By.XPATH,"./../span[2]");
                        icon=element.get_attribute("class")
                        if ("finish-tig" in icon) :
                            print "已学完".encode("gb18030")
                            continue
                    except:
                        pass
                    #切换2.0倍速播放
                    
                    #等待观看时间完成
                    checktime();
                    #随机等待一段时间
                    randomsleep();
#不点下一节按钮，直接通过点击下一个列表来切换
#            try:
#                time.sleep(2)
#                #<button data-v-0d38406a="" class="next-button">下一节</button>
#                element = WebDriverWait(browser, 10).until(
#                    EC.presence_of_element_located((By.CLASS_NAME, "next-button"))   #20190212现在好像都学完了以后改成弹出一个确定按钮了
#                )
#                element.click()
#            except Exception as btnerr:
#                errmsg=traceback.format_exc()
#                print '下一节'.encode("gb18030"),errmsg.encode("gb18030")
            
#            try:
#                time.sleep(2)
#                element = WebDriverWait(browser, 10).until(
#                    EC.presence_of_element_located((By.CLASS_NAME, "layui-layer-btn1"))   #弹出窗口下一步
#                )
#                element.click()
#            except :
#                time.sleep(2)
#                element = WebDriverWait(browser, 60).until(
#                    EC.presence_of_element_located((By.CLASS_NAME, "cs-menu-link"))  #课程学习
#                )
#                element.click()
#                time.sleep(2)
#                element = WebDriverWait(browser, 10).until(
#                    EC.presence_of_element_located((By.ID, "goNextStep"))   #下一步
#                )
#                element.click()
            
            
#            finally:
#                pass
        except Exception, err:
                errmsg=traceback.format_exc()
                print '处理sub错误: '.encode("gb18030"),errmsg.encode("gb18030")

        #退出iframe
        browser.switch_to.default_content()
        #评分
        print "评分".encode("gb18030")
        try:
            time.sleep(stepSleepSecond)
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.XPATH,"//p[@class='cs-eval-score']/input[5]"))  #评分5星
            )
            element.click()
            
            time.sleep(stepSleepSecond)
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.ID, "courseEvaluateSubmit"))  #提交
            )
            element.click()
            time.sleep(stepSleepSecond)
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.CLASS_NAME, "layui-layer-btn1"))  #提交
            )
            element.click()
            time.sleep(stepSleepSecond)
            element = WebDriverWait(browser, stepSleepSecond).until(
                EC.presence_of_element_located((By.CLASS_NAME, "elpui-layer-btn0"))  #查看结果 only-one-btn 
            )
            element.click()
        except Exception, e:
            errmsg=traceback.format_exc()
            print '评分过程报错，可能不需要评分，直接关闭课程页面，从课程列表选择下一门课程，错误信息: '.encode("gb18030"),errmsg.encode("gb18030")
        browser.close()

        time.sleep(stepSleepSecond)

    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        pass

    finally:
        pass
        
browser.quit()

