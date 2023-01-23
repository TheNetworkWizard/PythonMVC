from Lib import Model

import logging
import json

logger = logging.getLogger(__name__)


class Index_model(Model):
    def __init__(self):
        super().__init__()

    def getDashboard(self):
        devicesArray = {}
        sites = super(Index_model, self).selectQuery("select site_name from tbl_site")
        for site in sites:
            devicesArray[site['site_name']] = {}
            strSQL = f"SELECT *, (SELECT MIN(device_status) FROM tbl_device where device_location = tl.location_id) AS 'device_status', (SELECT MIN(port_status) FROM tbl_device td INNER JOIN tbl_port tp ON td.device_id = tp.device_id WHERE td.device_location = tl.location_id) AS 'port_status' FROM tbl_location tl join tbl_site ts on tl.location_site = ts.site_id WHERE ts.site_name = '{site['site_name']}' order by location_name"
            cabinets = super(Index_model, self).selectQuery(strSQL)
            for cabinet in cabinets:
                devicesArray[site['site_name']][cabinet['location_name']] = {}
                devicesArray[site['site_name']][cabinet['location_name']]['location_name'] = cabinet['location_name']
                devicesArray[site['site_name']][cabinet['location_name']]['location_description'] = cabinet['location_description']
                devicesArray[site['site_name']][cabinet['location_name']]['device_status'] = cabinet['device_status']
                devicesArray[site['site_name']][cabinet['location_name']]['port_status'] = cabinet['port_status']
            
        return devicesArray
    
    def getDeviceIssues(self):
        strSQL = "SELECT distinct device_name, (select site_name from tbl_site ts where ts.site_id = td.device_site) as 'device_site', (select location_name from tbl_location tl where tl.location_id = td.device_location and location_site = td.device_site) as 'device_location', device_ip, device_type_name, device_status from (tbl_device td join tbl_device_type tdt on td.device_type = tdt.device_type) left join tbl_port tp on td.device_id = tp.device_id where device_status = 0"

        issues = super(Index_model, self).selectQuery(strSQL)

        return issues


    def getInterfaceIssues(self):
        strSQL = "SELECT device_name, (select site_name from tbl_site ts where ts.site_id = td.device_site) as 'device_site', (select location_name from tbl_location tl where tl.location_id = td.device_location and location_site = td.device_site) as 'device_location', device_ip, device_type_name, device_status, port_name, port_status from (tbl_device td join tbl_device_type tdt on td.device_type = tdt.device_type) left join tbl_port tp on td.device_id = tp.device_id where port_status = 0"

        issues = super(Index_model, self).selectQuery(strSQL)

        return issues

        
        """
        for site in sites:
            
            cabinets = super(Index_model, self).selectQuery(f"SELECT * FROM tbl_location WHERE location_site = {site['site_id']}")
            for cabinet in cabinets:
                strSQL = f"select device_name, device_ip, device_status, port_name, port_status from tbl_device td left join tbl_port tp on td.device_id = tp.device_id where device_status = 0 or port_status = 0 and device_site = { site['site_id'] } and device_location = { cabinet['location_id'] };"
                #logger.debug(strSQL)
                #strSQL = f"select device_name, device_ip, device_status, port_name, port_status from tbl_device td left join tbl_port tp on td.device_id = tp.device_id where device_status = 0 or port_status = 0;"
                devices = super(Index_model, self).selectQuery(strSQL)
                #logger.debug(devices)
                for device in devices:
                    if(not site['site_name'] in devicesArray):
                        devicesArray[site['site_name']] = {}

                    if(not cabinet['location_name'] in devicesArray[site['site_name']]):
                        devicesArray[site['site_name']][cabinet['location_name']] = {}

                    devicesArray[site['site_name']][cabinet['location_name']]['location_name'] = cabinet['location_name']
                    devicesArray[site['site_name']][cabinet['location_name']]['location_description'] = cabinet['location_description']
                    
                    if(not 'devices' in devicesArray[site['site_name']][cabinet['location_name']]):
                        devicesArray[site['site_name']][cabinet['location_name']]['devices'] = {}
                        
                    if(not device['device_name'] in devicesArray[site['site_name']][cabinet['location_name']]['devices']):                    
                        devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']] = {}
                        devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']]['ports'] = {}
                        
                    devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']]['device_name'] = device['device_name'] 
                    devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']]['device_ip'] = device['device_ip'] 
                    devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']]['device_status'] = device['device_status']
                    devicesArray[site['site_name']][cabinet['location_name']]['devices'][device['device_name']]['ports'][device['port_name']] = device['port_status']
        """     

        return devicesArray