/* VU Amsterdam, Social AI Group
 * Bilgin Aveno�lu, 10/03/2020 */

package sic.db;

import java.io.IOException;
import org.redisson.api.RLiveObjectService;
import org.redisson.api.RedissonClient;
import sic.Device;
import sic.ServiceRequest;
import sic.User;
import sic.EndPoint;
import sic.ProtocolType;
import sic.Sensor;
import sic.Service;
import sic.redis.GetRedisService;

public class BatchDeviceInsert {

	public static void main(String[] args) throws IOException {
		GetRedisService redisService = new GetRedisService();
		RedissonClient redisson = redisService.getRedisson();
		RLiveObjectService liveObjectService = redisson.getLiveObjectService();

		Service searchedService1 = liveObjectService.get(Service.class, "EmotionRecognition");
		if (searchedService1 != null)
			liveObjectService.delete(searchedService1);
		
		User searchedUser1 = liveObjectService.get(User.class, "Bilgin");
		if (searchedUser1 != null)
			liveObjectService.delete(searchedUser1);

		Device searchedDevice1 = liveObjectService.get(Device.class, "BilginPhone1");
		if (searchedDevice1 != null)
			liveObjectService.delete(searchedDevice1);
			
		Service service1 = new Service("EmotionRecognition");
		service1 = liveObjectService.merge(service1);
			EndPoint rcvEndPointSrv1 = new EndPoint("EmotionRecognitionRcv");
			rcvEndPointSrv1.setProtocolType(ProtocolType.REDIS);
			rcvEndPointSrv1.setIpNumber("10.98.98.61");
			rcvEndPointSrv1.setPortNumber("6379");
			//rcvEndPointSrv1.setWebURI("http://10.98.98.62:5000/Result");
			rcvEndPointSrv1 = liveObjectService.merge(rcvEndPointSrv1);
			service1.setRcvEndPoint(rcvEndPointSrv1);
			EndPoint sndEndPointSrv1 = new EndPoint("EmotionRecognitionSnd");
			sndEndPointSrv1.setProtocolType(ProtocolType.HTTP);
			//sndEndPointSrv1.setWebURI("http://10.98.98.62:5000/Result");
			//sndEndPointSrv1.setIpNumber("10.98.98.61");
			//sndEndPointSrv1.setPortNumber("6379");
			sndEndPointSrv1 = liveObjectService.merge(sndEndPointSrv1);
			service1.setSndEndPoint(sndEndPointSrv1);		
				
		User user1 = new User("Bilgin");
		user1 = liveObjectService.merge(user1);

			Device phone1 = new Device("BilginPhone1");
			phone1 = liveObjectService.merge(phone1);
			phone1.setUser(user1);
			phone1.setIsConnected(false);
			user1.getDevices().add(phone1);
	
				Sensor phone1Sensor1 = new Sensor("BilginPhone1Camera1");
				phone1Sensor1 = liveObjectService.merge(phone1Sensor1);
				phone1Sensor1.setDevice(phone1);
				phone1.getSensors().add(phone1Sensor1);
		
					EndPoint phone1Sen1SndEndPoint = new EndPoint("BilginPhone1Camera1Snd");
					phone1Sen1SndEndPoint.setProtocolType(ProtocolType.HTTP);
					phone1Sen1SndEndPoint = liveObjectService.merge(phone1Sen1SndEndPoint);
					phone1Sensor1.setSndEndPoint(phone1Sen1SndEndPoint);
				
					ServiceRequest phone1Sen1SrvReq1 = new ServiceRequest("BilginPhone1Camera1EmotionRecognition");
					phone1Sen1SrvReq1 = liveObjectService.merge(phone1Sen1SrvReq1);
					phone1Sen1SrvReq1.setService(service1);
					phone1Sen1SrvReq1.setSensor(phone1Sensor1);
					phone1Sensor1.getServiceRequests().add(phone1Sen1SrvReq1);
			
						EndPoint phone1Sen1SerReq1RcvEndPoint = new EndPoint("BilginPhone1Camera1EmotionRecognitionRcv1");
						phone1Sen1SerReq1RcvEndPoint.setProtocolType(ProtocolType.HTTP);
						phone1Sen1SerReq1RcvEndPoint.setWebURI("http://10.98.98.62:5000/");
						phone1Sen1SerReq1RcvEndPoint = liveObjectService.merge(phone1Sen1SerReq1RcvEndPoint);
						phone1Sen1SrvReq1.getSenSrvReqRcvEndPoints().add(phone1Sen1SerReq1RcvEndPoint);
			
		System.out.println("Database is Created!");

		redisson.shutdown();
	}
}
