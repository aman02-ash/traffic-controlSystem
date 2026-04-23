import React from 'react';
import { getVideoFeedUrl } from '../services/api';

const LaneCard = ({ laneId, laneData, isActive }) => {
  const { counts, score, congestionLevel } = laneData || {
    counts: { car: 0, motorcycle: 0, bus: 0, truck: 0 },
    score: 0,
    congestionLevel: 'N/A',
  };

  return (
    <div className={`lane-card ${isActive ? 'active' : ''}`}>
      <div className="lane-header">
        <h3>{laneId.replace('_', ' ').toUpperCase()}</h3>
        <span className={`congestion-badge ${congestionLevel.toLowerCase()}`}>
          {congestionLevel}
        </span>
      </div>
      <div className="video-feed">
        <img
          src={getVideoFeedUrl(laneId)}
          alt={`${laneId} live feed`}
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/320x180?text=No+Feed+Available';
          }}
        />
      </div>
      <div className="lane-stats">
        <div className="counts-grid">
          <div className="count-item">
            <span className="count-label">Cars:</span>
            <span className="count-value">{counts.car}</span>
          </div>
          <div className="count-item">
            <span className="count-label">Motorcycles:</span>
            <span className="count-value">{counts.motorcycle}</span>
          </div>
          <div className="count-item">
            <span className="count-label">Buses:</span>
            <span className="count-value">{counts.bus}</span>
          </div>
          <div className="count-item">
            <span className="count-label">Trucks:</span>
            <span className="count-value">{counts.truck}</span>
          </div>
        </div>
        <div className="score-display">
          <span className="score-label">Lane Score:</span>
          <span className="score-value">{score}</span>
        </div>
      </div>
    </div>
  );
};

export default LaneCard;
