package com.smarttraffic.trafficcontrol.dto;

import java.util.Map;

public class LaneStateDTO {

    private Map<String, Integer> counts;  // 🔥 NEW
    private int score;
    private String congestionLevel;

    // ✅ Updated constructor
    public LaneStateDTO(Map<String, Integer> counts, int score, String congestionLevel) {
        this.counts = counts;
        this.score = score;
        this.congestionLevel = congestionLevel;
    }

    // ✅ Getters & Setters

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

    public String getCongestionLevel() {
        return congestionLevel;
    }

    public void setCongestionLevel(String congestionLevel) {
        this.congestionLevel = congestionLevel;
    }
}