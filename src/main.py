from model import UserModel, DeviceModel, DailyReportModel
from datetime import datetime


# passing admin as initialization parameter for current user defined in model
user_coll = UserModel('admin')
print(f'Does \'{user_coll.get_user_name()}\' have admin access?')
if(UserModel.authenticate_admin()==-1):
    print("False")
else:
    print("True")
print('')

print(f'Is username based query possible for \'{user_coll.get_user_name()}\'?')
user_document = user_coll.find_by_username('user_2')
if (user_document== -1):
    print(user_coll.latest_error)
else:
    print(user_document)
print('')

print(f'Can \'{user_coll.get_user_name()}\' add a new user?')
user_document = user_coll.find_by_username('user_2')
if (user_document== -1):
    print(user_coll.latest_error)
else:
    print(user_document)
print('')


# Initializing device search through a parameter using method defined in user model
device_coll = DeviceModel()
#device_id = 'DT201'
device_id = 'DH004'
print(f'Can \'{user_coll.get_user_name()}\' access device '+device_id+'?')
device_document = device_coll.find_device_id(device_id)
if (device_document ==-1):
    print(device_coll.latest_error)
else:
    print(device_document)
print('')

device_id = 'DT004'
print(f'Can \'{user_coll.get_user_name()}\' create a device '+device_id+'?')
device_document = device_coll.find_device_id(device_id)
if (device_document==-1):
    print(device_coll.latest_error)
else:
    print(device_document)
print('')

device_id = 'DT004'
print(f'Can \'{user_coll.get_user_name()}\' read '+device_id+' device data?')
device_document = device_coll.find_device_id(device_id)
if (device_document==-1):
    print(device_coll.latest_error)
else:
    print(device_document)
print('')

### generating Daily reports from weather data usng the method defined in model as generate report 
## with aggregated data using the method create_aggregate_data
report_coll = DailyReportModel()
report_coll.create_agg_data()

#date = datetime(2020, 12, 1, 0, 0)
date = '2020-12-01'
device_id='DT002'

print(f'Daily report by \'{user_coll.get_user_name()}\' for '+device_id+' device, dated: '+date+'')
report_document = report_coll.find_dev_by_datetime(device_id, date)
if (report_document==-1):
    print(report_coll.latest_error)
else:
    print(report_document)
print('')

#device_id='DT002'
#startdate = '2020-12-01'
#enddate = '2020-12-04'
#print(f'Can \'{user_coll.get_user_name()}\' access multiple data range report for '+device_id+'?')
#range_report_document = report_coll.find_dev_by_date_range(device_id, startdate, enddate)
#for i in range_report_document:
#    if (report_document==-1):
#        print(report_coll.latest_error)
#    else:
#        print(report_document)
#    print('')

## Daily report for multiple days using date range
device_id='DT002'
startdate = '2020-12-01'
enddate = '2020-12-04'
print(f'Aggregate report by \'{user_coll.get_user_name()}\' from '+startdate+' to '+enddate+' for '+device_id+'?')
range_report_document = report_coll.find_dev_by_date_range(device_id, startdate, enddate)
if (report_document==-1):
        print(report_coll.latest_error)
elif (report_document):
    for i in range_report_document:
        print(i)
    print('')
else:
    print("No Records Found")
    print('')


## To check if users have any admin access to read / write using the initialisation method
user_coll = UserModel('user_1')
print(f'Does \'{user_coll.get_user_name()}\' have admin access?')
if(UserModel.authenticate_admin()==-1):
    print("False")
    print('')
else:
    print("True")
    print('')


print(f'Is username based query possible for \'{user_coll.get_user_name()}\'?')
user_document = user_coll.find_by_username('user_2')
if (user_document== -1):
    print(user_coll.latest_error)
else:
    print(user_document)
print('')

username = 'user_4'
email = 'someone@email.com'
role='user'
print(f'Can \'{user_coll.get_user_name()}\' add a new user?')
user_document = user_coll.insert(username, email, role)
if (user_document== -1):
    print(user_coll.latest_error +'  cannot insert new user '+username+'')
else:
    print(user_document)
print('')


# This section of the program is to initiate and search inside device collection using a device id
device_coll = DeviceModel()
device_id = 'DT004'
print(f'Can \'{user_coll.get_user_name()}\' access device '+device_id+'?')
device_document = device_coll.find_device_id(device_id)
if (device_document ==-1):
    print(device_coll.latest_error)
    print('')
else:
    print(device_document)
print('')

device_id = 'DT008'
desc = 'Temperature  Sensor'
type='Temperature'
manufacturer = 'Acme'
print(f'Can \'{user_coll.get_user_name()}\' create a device '+device_id+'?')
device_document = device_coll.insert(device_id,desc, type, manufacturer)
if (device_document==-1):
    print(device_coll.latest_error + ' cannot create new device '+device_id+'')
    print('')
else:
    print(device_document)
print('')

device_id = 'DT001'
print(f'Can \'{user_coll.get_user_name()}\' read '+device_id+' device data?')
device_document = device_coll.find_device_id(device_id)
if (device_document==-1):
    print(device_coll.latest_error)
    print('')
else:
    print(device_document)
print('')

device_id = 'DT007'
print(f'Can \'{user_coll.get_user_name()}\' read '+device_id+' device data?')
device_document = device_coll.find_device_id(device_id)
if (device_document==-1):
    print(device_coll.latest_error)
    print('')
else:
    print(device_document)
print('')

