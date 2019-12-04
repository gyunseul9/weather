
'''
CREATE TABLE weather (
  num int(11) NOT NULL AUTO_INCREMENT,
  mdate varchar(50) NOT NULL,
  src varchar(50) NOT NULL,
  area varchar(50) NOT NULL,
  state varchar(50) DEFAULT '-',
  temp varchar(50) DEFAULT '-',
  dis varchar(50) DEFAULT '-',
  rain varchar(50) DEFAULT '-',
  hum varchar(50) DEFAULT '-',
  wdir varchar(255) DEFAULT '-',
  wspeed varchar(255) DEFAULT '-',
  hpa varchar(255) DEFAULT '-',
  posted datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='HOST',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='HOST',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
  