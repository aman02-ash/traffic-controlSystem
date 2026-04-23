package com.smarttraffic.trafficcontrol.dto;

import java.util.Map;

public class LaneData {
    private Map<String, Integer> counts;
    private int score;

    public Map<String, Integer> getCounts() {
        return counts;
    }

    public void setCounts(Map<String, Integer> counts) {
        this.counts = counts;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }
}
