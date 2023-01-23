from Lib import Model

import os
import hashlib
import time

import logging
import ldap
logger = logging.getLogger(__name__)


class Account_model(Model):

    ldap_fail = ""

    def __init__(self):
        super().__init__()
        logger.debug("Account Model Loaded")

    def loginUser(self, username, password):
        logger.debug(f"LoginUser: {username}")
        """strSQL = f"SELECT user_enc_password, user_salt from user_table where username = '{username}'"
        result = super().selectQuery(strSQL)
        encoded_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes(result[0][1]), 100000)
        try:
            assert result[0][0] == encoded_password
            strSQL = f"SELECT user_id from user_table where username = '{username}'"
            return super().selectQuery(strSQL)
        except:
            return False
            """
        
        ldap_server="ldap://xqehkl.nhs.uk"
        try:
            conn = ldap.initialize(ldap_server)
            conn.protocol_version = 3
            conn.set_option(ldap.OPT_REFERRALS, 0)
            
            conn.simple_bind_s('QEH\\' + username , password)
            
            base_dn = "OU=01 - QEH,DC=xqehkl,DC=nhs,DC=uk"

            filter = "(&(sAMAccountName=%s)(memberOf=CN=Network,OU=ICT,OU=09 - Distribution Groups,DC=xqehkl,DC=nhs,DC=uk))" % (username)
            
            result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, ['cn'])
            if(len(result) == 1):
                userLevel = 2
                conn.unbind_s()
                logger.debug("LDAP Success - Networks")
                return userLevel
            else:
                filter = "(&(sAMAccountName=%s)(memberOf=CN=ICT Department,OU=08 - Security Groups,DC=xqehkl,DC=nhs,DC=uk))" % (username)
                
                result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, ['cn'])
                if(len(result) == 1):
                    userLevel = 1
                    conn.unbind_s()
                    logger.debug("LDAP Success - ICT")
                    return userLevel
                else:
                    conn.unbind_s()
                    self.ldap_fail = "User not found in AD groups"
                    logger.debug("LDAP Fail - Not found in group")
                    return False
        except Exception as error:
            #print()
            self.ldap_fail = str(error)
            logger.debug(f"LDAP Fail {str(error)}")
            return False

    def getLDAPFailureReason(self):
        return self.ldap_fail

    def createSession(self, username, userLevel):
        logger.debug(f"Creating session for {username}")
        duration = 7776000
        hashString = (str(time.time()) + username).encode('utf-8')
        logger.debug(hashString)
        sid = hashlib.sha1(hashString).hexdigest()
        logger.debug(f"Generated {sid} for {username}")
        try:
            logger.debug(f"Deleting old sessions for {username}")
            strSQL = f"DELETE FROM tbl_sessions where userID = '{username}'"
            super(Account_model, self).deleteQuery(strSQL)
            
            logger.debug(f"Creating session for {username}")
            strSQL = f"INSERT INTO tbl_sessions (sid, userID, userLevel, expires) VALUES ('{sid}', '{username}', {userLevel}, {time.time() + duration})"
            super(Account_model, self).insertQuery(strSQL)
            return sid
        except Exception as error:
            logger.debug(str(error))
            return False
        