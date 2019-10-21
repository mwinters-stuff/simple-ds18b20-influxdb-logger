from influxdb import InfluxDBClient
import ds18b20
import argparse

def post_to_influxdb(args, temperature):
    dbclient = InfluxDBClient(args.hostname, args.port, args.username, args.password, args.database)
    influx_data = [{
        'measurement': args.measurement,
        'tags': {
           'sensor': 'environmental',
           'location': args.location
        },
        'fields': {
            'temperature': temperature
        }
    }]

    print ('Influx Data: ', influx_data)
    dbclient.write_points(influx_data)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='DS18B20 data logger to influxdb')
  parser.add_argument('--hostname', action='store', default='localhost', help='InfluxDB hostname')
  parser.add_argument('--port', action='store', type=int, default=8086, help='InfluxDB port')
  parser.add_argument('--username', action='store', default='root', help='InfluxDB username')
  parser.add_argument('--password', action='store', default='root', help='InfluxDB password')
  parser.add_argument('--database', action='store', required=True, help='InfluxDB database')
  parser.add_argument('--measurement', action='store', required=True, help='Sensor measurement')
  parser.add_argument('--location', action='store', required=True, help='Sensor location')

  args = parser.parse_args()
  print(args)
  
  tsen = ds18b20.DS18B20()
  temperature = tsen.read_temp();
  print (temperature)
  post_to_influxdb(args, temperature)

