# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self, activeUser):
        self._db = Database()
        self._latest_error = ''
        key = {'username': activeUser}
        UserModel._activeUser = self.__find(key)
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        if(self._activeUser['role']=='admin'):
            key = {'username': username}
            return self.__find(key)
        else:
            self._latest_error = f'Query failed, Admin access required!'
            return -1
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        if(self._activeUser['role']=='admin'):
            key = {'_id': ObjectId(obj_id)}
            return self.__find(key)
        else:
            self._latest_error = f'Query failed, Admin access required!'
            return -1
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
            user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
            return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role):
        if(self._activeUser['role']=='admin'):
            self._latest_error = ''
            user_document = self.find_by_username(username)
            if (user_document):
                self._latest_error = f'Username {username} already exists'
                return -1

            user_data = {'username': username, 'email': email, 'role': role}
            user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
            return self.find_by_object_id(user_obj_id)
        else:
            self._latest_error = f'Insert failed, Admin access required!'
            return -1

    def authenticate_admin():
        if(UserModel._activeUser['role']=='admin'):
            return 1
        else:
            UserModel._latest_error = f'False'
            return -1

    def access_device_id(did):
        if (UserModel.authenticate_admin()==1):
            return ['rw']
        else:
            access = [a['atype'] for a in UserModel._activeUser['alist'] if a['did'] == did]
            if len(access) == 0:
                return ['']
            else:
                return access

    def get_user_name(self):
        return self._activeUser['username']

    def is_user_current(self):
        return self._activeUser

# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        #self._activeUser = activeUser
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_device_id(self, device_id):
        if (UserModel.access_device_id(device_id)[0] == 'r' or UserModel.access_device_id(device_id)[0] == 'rw'):
            key = {'device_id': device_id}
            document = self.__find(key)
            if (document):
                return document
            else:
                self._latest_error = f'Device not found'
                return -1

        else:
            self._latest_error = f'Read access not allowed to '+device_id
            return -1

    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        if(UserModel.access_device_id(device_id)[0] == 'rw'):
            self._latest_error = ''
            device_document = self.find_device_id(device_id)
            if (device_document):
                self._latest_error = f'Device id {device_id} already exists'
                return -1

            device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
            device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
            return self.find_by_object_id(device_obj_id)
        else:
            self._latest_error = f'Insert failed, Admin access required!'
            return -1


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_dev_by_datetime(self, device_id, timestamp):
        if (UserModel.access_device_id(device_id)[0] == 'r' or UserModel.access_device_id(device_id)[0] == 'rw'):
            key = {'device_id': device_id, 'timestamp': timestamp}
            return self.__find(key)
        else:
            self._latest_error = f'Read access not allowed to '+device_id+' data'
            return -1
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates 
    #latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        if(UserModel.access_device_id(device_id)[0] == 'rw'):
            self._latest_error = ''
            wdata_document = self.find_dev_by_datetime(device_id, timestamp)
            if (wdata_document):
                self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
                return -1

            weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
            wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
            return self.find_by_object_id(wdata_obj_id)
        else:
            self._latest_error = ''
            print(f'Write access not allowed to '+device_id+' data')
            return -1


# Report collection document contains device_id (String), average (int), min (int), max(int) fields
class DailyReportModel:
    DAILY_REPORT_COLLECTION = 'daily_reports'
    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        report_document = self._db.get_single_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        return report_document

    def __findAll(self, key):
        report_document = self._db.get_all_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        return report_document

    def insert(self, device_id, avg, max, min, timestamp):
        self._latest_error = ''
        if(self.find_dev_by_datetime(device_id,timestamp)):
            self._latest_error = f'Report for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        report_record = {
            'device_id': device_id,
            'average': avg,
            'minimum': max,
            'maximum': min,
            'date': timestamp
        }
        rdata_obj_id = self._db.insert_single_data(DailyReportModel.DAILY_REPORT_COLLECTION, report_record)
        return self.find_by_object_id(rdata_obj_id)

    def generatereport(self,device,startdate,endate):
        pass

    def create_agg_data(self):
        key=[{'$group': 
        {'_id': {'device_id': '$device_id','timestamp': {'$dateToString': {'format': '%Y-%m-%d','date': '$timestamp'}}},
        'average': {'$avg': '$value'},'minimum': {'$min': '$value'},'maximum': {'$max': '$value'}}}]
        #weather_coll = WeatherDataModel()
        daily_report_cols = self._db.aggregate(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        for agg_data_coll in daily_report_cols:
            daily_rep_data=self.insert(agg_data_coll['_id']['device_id'], agg_data_coll['average'], agg_data_coll['minimum'], 
                agg_data_coll['maximum'], agg_data_coll['_id']['timestamp'])

     #search by device id and timestamp
    def find_dev_by_datetime(self, device_id, timestamp):
        if (UserModel.access_device_id(device_id)[0] == 'r' or UserModel.access_device_id(device_id)[0] == 'rw'):
            key = {'device_id': device_id, 'date': timestamp}
            return self.__find(key)
        else:
            self._latest_error = f'Read ka access not allowed to '+device_id+' data'
            return -1
            
    def find_dev_by_date_range(self, device_id, starttimestamp, endtimestamp):
        if (UserModel.access_device_id(device_id)[0] == 'r' or UserModel.access_device_id(device_id)[0] == 'rw'):
            key = {'device_id' : device_id, 'date' : {'$gte' : starttimestamp, '$lte' : endtimestamp }}
            return self.__findAll(key)
        else:
            self._latest_error = f'Read ka access not allowed to '+device_id+' data'
            return -1
            