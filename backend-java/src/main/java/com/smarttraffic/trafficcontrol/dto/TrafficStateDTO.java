package com.smarttraffic.trafficcontrol.dto;

import java.util.Map;

public class TrafficStateDTO {
    private Map<String, LaneStateDTO> laneStates;
    private String activeGreenLane;
    private int timer;

    public TrafficStateDTO(Map<String, LaneStateDTO> laneStates, String activeGreenLane, int timer) {
        this.laneStates = laneStates;
        this.activeGreenLane = activeGreenLane;
        this.timer = timer;
    }

    public Map<String, LaneStateDTO> getLaneStates() {
        return laneStates;
    }

    public void setLaneStates(Map<String, LaneStateDTO> laneStates) {
        this.laneStates = laneStates;
    }

    public String getActiveGreenLane() {
        return activeGreenLane;
    }

    public void setActiveGreenLane(String activeGreenLane) {
        this.activeGreenLane = activeGreenLane;
    }

    public int getTimer() {
        return timer;
    }

    public void setTimer(int timer) {
        this.timer = timer;
    }
}
