import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriverbase import BaseTest
from Admin_Portal import AdminPortalTest1, AdminPortalTest1stPage, AdminPortalTest2ndPage, Login_Page
from CustomerPortal import SupportPortalPage
import org.testng.Assert
import logging

class CommonTests1(BaseTest):
    
    def __init__(self):
        super().__init__()
        self.hploginpage = None
        self.hpSupportPortalPage = None
        self.hpAdminPortalTest1 = None
        self.hpAdminPortalTest2 = None
        
    AdminPortalURL = "https://interview.supporthive.com/staff"
    SupportTicketURL = "https://interview.supporthive.com/new/"
    browser = "Chrome"
    username = "interview_agent"
    password = "Interview@123"
    statusName = "Issue created"
    priorityName = "Assistance required"
    Subject = "Test Ticket raised by XYZ"
    Message = "Hi, i am having certain issues in the Happy fox portal. Can you please help me."
    FullName = "Reese Harrold"
    Email = "testno100@gmail.com"
    
    def login_as_admin(self):
        try:
            logging.info("Start of LoginAsAdmin")
            self.hploginpage = Login_Page(self.get_driver())
            self.hploginpage.navigate_to_happyfox_home_page_url(self.AdminPortalURL)
            self.hploginpage.enter_username(self.username)
            logging.info("username entered")
            self.hploginpage.enter_password(self.password)
            logging.info("password entered")
            self.hploginpage.click_login_button()
            logging.info("login clicked")
            self.hpAdminPortalTest1 = self.hploginpage.validate_pending_tickets_title()
            Assert.pass("Login completed successfully")
        except Exception as e:
            logging.error(e)
            Assert.fail("Error in login_as_admin: " + str(e))
    
    def creating_support_ticket(self):
        try:
            logging.info("Start of Client support ticket")
            self.hpSupportPortalPage = SupportPortalPage(self.get_driver())
            self.hpSupportPortalPage.navigate_to_happyfox_support_portal_url(self.SupportTicketURL)
            self.hpSupportPortalPage.enter_subject(self.Subject)
            self.hpSupportPortalPage.enter_message(self.Message)
            self.hpSupportPortalPage.click_add_cc()
            self.hpSupportPortalPage.click_add_bcc()
            self.hpSupportPortalPage.enter_full_name(self.FullName)
            self.hpSupportPortalPage.enter_email(self.Email)
            self.hpAdminPortalTest2 = self.hpSupportPortalPage.click_create_ticket()
            logging.info("Ticket created")
            self.hpAdminPortalTest2.goto_agent_portal()
            Assert.pass("Ticket created successfully")
        except Exception as e:
            logging.error(e)
            Assert.fail("Error in creating_support_ticket: " + str(e))
    
    def test_case_1(self):
        try:
            logging.info("Start of test case 1")
            self.hpAdminPortalTest1 = self.hploginpage.validate_pending_tickets_title()
            self.hpAdminPortalTest1.click_status()
            self.hpAdminPortalTest1.click_new_status()
            logging.info("New Status process started")
            self.hpAdminPortalTest1.enter_status_name(self.statusName)
            logging.info("status name entered")
            # self.hpAdminPortalTest1.enter_status_colour("#21d0d5") //#21d0d5 skyblue, #21d567 green
            logging.info("colour set")
            self.hpAdminPortalTest1.enter_behavior("Pending")
            self.hpAdminPortalTest1.enter_status_description("Status when a new issue ticket is created in HappyFox")
            logging.info("description added")
            self.hpAdminPortalTest1.click_add_status()
            logging.info("Status added")
            self.hpAdminPortalTest1.set_default_status(self.statusName)
            self.hpAdminPortalTest1.click_priority_section()
            self.hpAdminPortalTest1.click_new_priority()
            logging.info("New priority process started")
            self.hpAdminPortalTest1.enter_priority_name(self.priorityName)
            self.hpAdminPortalTest1.enter_priority_description("Priority of the newly created tickets")
            self.hpAdminPortalTest1.enter_priority_help_text("priority helptext")
            self.hpAdminPortalTest1.click_add_priority()
            self.hpAdminPortalTest1.set_default_priroity(self.priorityName)
            logging.info("Priority added")
        except Exception as e:
            logging.error(e)
    
    def test_case_2(self):
        try:
            logging.info("Start of test case 2")
            self.creating_support_ticket()
            self.hploginpage.validate_pending_tickets_title1()
            self.hpAdminPortalTest2.click_pending_tickets()
            logging.info("Pending tickets clicked")
            self.hpAdminPortalTest2.open_customer_ticket(self.Subject)
            
            # Assertion of the Priority and Status of the ticket created 
            Assert.assertEquals(self.hpAdminPortalTest2.get_contact_name(),"Aravind") 
            Assert.assertEquals(self.hpAdminPortalTest2.get_email_txt(),self.Email)
            
            self.hpAdminPortalTest2.click_reply_button()
            Assert.assertEquals(self.hpAdminPortalTest2.get_status_txt(),self.statusName)
            Assert.assertEquals(self.hpAdminPortalTest2.get_priority_txt(),self.priorityName.upper())
            
            self.hpAdminPortalTest2.click_canned_action()
            self.hpAdminPortalTest2.click_search_canned_action("Reply to Customer Query")
            self.hpAdminPortalTest2.click_apply_canned_action()
            
            # Assertion of the Priority and Status of the ticket after edition
            Assert.assertEquals(self.hpAdminPortalTest2.get_status_txt(),"Closed")
            Assert.assertEquals(self.hpAdminPortalTest2.get_priority_txt(),"Medium")
            self.hpAdminPortalTest2.send_reply() 
            self.hpAdminPortalTest1 = self.hpAdminPortalTest2.close_the_ticket()
            self.hpAdminPortalTest1.click_priorities()
            logging.info("Test Case 2 over")
        except Exception as e:
            logging.info(e)
    
    def test_case_3(self):
        try:
            logging.info("Start of test case 3")
            self.hpAdminPortalTest1.set_default_priroity("Low")
            logging.info("Default priority set as Low")
            self.hpAdminPortalTest1.click_added_priority(self.priorityName)
            logging.info("Priority clicked")
            self.hpAdminPortalTest1.click_priority_delete_link()
            self.hpAdminPortalTest1.click_delete_confirm()
            logging.info("Priority deleted")  
            self.hpAdminPortalTest1.click_statuses_section()
            self.hpAdminPortalTest1.set_default_status("New")
            logging.info("Default status set as New")
            self.hpAdminPortalTest1.click_added_status(self.statusName)
            logging.info("Statuses clicked")
            self.hpAdminPortalTest1.click_status_delete_link()
            # self.hpAdminPortalTest1.set_new_default_status()
            self.hpAdminPortalTest1.click_delete_confirm()
            logging.info("Statuses deleted")  
            self.hpAdminPortalTest1.click_profile()
            self.hpAdminPortalTest1.click_logout()
            logging.info("Logged out successfully")
        except Exception as e:
            logging.error(e)
    
if __name__ == "__main__":
    common_tests = CommonTests1()
    common_tests.setup()
    common_tests.login_as_admin()
    common_tests.test_case_1()
    common_tests.test_case_2()
    common_tests.test_case_3()
    common_tests.teardown()
