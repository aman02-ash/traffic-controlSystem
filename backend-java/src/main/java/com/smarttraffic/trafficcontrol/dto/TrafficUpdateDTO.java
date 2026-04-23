package com.smarttraffic.trafficcontrol.dto;

import java.util.Map;

public class TrafficUpdateDTO {
    private Map<String, LaneData> lanes;

    public Map<String, LaneData> getLanes() {
        return lanes;
    }

    public void setLanes(Map<String, LaneData> lanes) {
        this.lanes = lanes;
    }
}
