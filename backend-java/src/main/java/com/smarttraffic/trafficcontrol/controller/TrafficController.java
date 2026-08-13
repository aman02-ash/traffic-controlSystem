package com.smarttraffic.trafficcontrol.controller;

import com.smarttraffic.trafficcontrol.dto.TrafficStateDTO;
import com.smarttraffic.trafficcontrol.dto.TrafficUpdateDTO;
import com.smarttraffic.trafficcontrol.service.TrafficControlService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
@RequestMapping("/traffic")
public class TrafficController {

    private final TrafficControlService trafficControlService;

    public TrafficController(TrafficControlService trafficControlService) {
        this.trafficControlService = trafficControlService;
    }

    @PostMapping("/update")
    public ResponseEntity<Void> updateTrafficData(@RequestBody TrafficUpdateDTO trafficUpdateDTO) {
        trafficControlService.updateTrafficData(trafficUpdateDTO);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/state")
    public ResponseEntity<TrafficStateDTO> getTrafficState() {
        return ResponseEntity.ok(trafficControlService.getTrafficState());
    }
}
