package com.smarttraffic.trafficcontrol;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.beans.factory.annotation.Autowired;
import com.smarttraffic.trafficcontrol.service.TrafficControlService;

@SpringBootApplication
@EnableScheduling // Enable scheduling for timer decrement
public class SmartTrafficControlSystemApplication {

    @Autowired
    private TrafficControlService trafficControlService;

    @Scheduled(fixedRate = 1000) // Decrement every second
    public void decrementTrafficTimer() {
        trafficControlService.decrementTimer();
    }

    public static void main(String[] args) {
        SpringApplication.run(SmartTrafficControlSystemApplication.class, args);
    }
}
