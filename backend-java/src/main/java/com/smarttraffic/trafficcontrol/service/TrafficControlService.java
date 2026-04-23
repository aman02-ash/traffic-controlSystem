package com.smarttraffic.trafficcontrol.service;

import com.smarttraffic.trafficcontrol.dto.LaneData;
import com.smarttraffic.trafficcontrol.dto.LaneStateDTO;
import com.smarttraffic.trafficcontrol.dto.TrafficStateDTO;
import com.smarttraffic.trafficcontrol.dto.TrafficUpdateDTO;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@Service
public class TrafficControlService {

    private final Map<String, LaneData> currentLaneData = new ConcurrentHashMap<>();
    private String activeGreenLane = "lane_1";
    private final AtomicInteger timer = new AtomicInteger(0);

    private static final int MIN_GREEN_TIME = 10;
    private static final int MAX_GREEN_TIME = 45;
    private static final int BASE_GREEN_TIME = 10;
    private static final int SCORE_MULTIPLIER = 2;

    public void updateTrafficData(TrafficUpdateDTO trafficUpdateDTO) {
        currentLaneData.putAll(trafficUpdateDTO.getLanes());
        determineActiveGreenLane();
    }

    public TrafficStateDTO getTrafficState() {
        Map<String, LaneStateDTO> laneStates = new HashMap<>();

        for (Map.Entry<String, LaneData> entry : currentLaneData.entrySet()) {
            String laneId = entry.getKey();
            LaneData data = entry.getValue();
            String congestionLevel = calculateCongestionLevel(data.getScore());

            laneStates.put(
                laneId,
                new LaneStateDTO(
                    data.getCounts(),
                    data.getScore(),
                    congestionLevel
                )
            );
        }

        return new TrafficStateDTO(laneStates, activeGreenLane, timer.get());
    }

    private void determineActiveGreenLane() {
        if (currentLaneData.isEmpty()) {
            return;
        }

        String highestScoreLane = currentLaneData.entrySet().stream()
            .max(Comparator.comparingInt(entry -> entry.getValue().getScore()))
            .map(Map.Entry::getKey)
            .orElse(activeGreenLane);

        if (!highestScoreLane.equals(activeGreenLane)) {
            activeGreenLane = highestScoreLane;

            LaneData data = currentLaneData.get(activeGreenLane);
            if (data != null) {
                timer.set(calculateGreenTime(data.getScore()));
            } else {
                timer.set(MIN_GREEN_TIME);
            }
        } else if (timer.get() == 0) {
            LaneData data = currentLaneData.get(activeGreenLane);
            if (data != null) {
                timer.set(calculateGreenTime(data.getScore()));
            } else {
                timer.set(MIN_GREEN_TIME);
            }
        }
    }

    private int calculateGreenTime(int score) {
        int greenTime = BASE_GREEN_TIME + score * SCORE_MULTIPLIER;
        return Math.min(MAX_GREEN_TIME, Math.max(MIN_GREEN_TIME, greenTime));
    }

    private String calculateCongestionLevel(int score) {
        if (score >= 50) {
            return "High";
        } else if (score >= 20) {
            return "Medium";
        } else {
            return "Low";
        }
    }

    public void decrementTimer() {
        if (timer.get() > 0) {
            timer.decrementAndGet();
        } else {
            determineActiveGreenLane();
        }
    }
}