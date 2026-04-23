import React from 'react';

const SignalPanel = ({ activeGreenLane, timer, mode }) => {
  return (
    <section className="signal-panel">
      <div className="signal-header">
        <h2>{mode || 'Adaptive Signal Control'}</h2>
        <div className="timer-display">
          <span className="timer-label">Next Switch:</span>
          <span className="timer-value">{timer}s</span>
        </div>
      </div>
      <div className="signal-status">
        <div className="active-lane-indicator">
          <span className="indicator-label">Active Green Lane:</span>
          <span className="indicator-value">{activeGreenLane ? activeGreenLane.replace('_', ' ').toUpperCase() : 'N/A'}</span>
        </div>
        <div className="traffic-light-ui">
          <div className={`light red ${activeGreenLane ? '' : 'active'}`}></div>
          <div className={`light yellow`}></div>
          <div className={`light green ${activeGreenLane ? 'active' : ''}`}></div>
        </div>
      </div>
    </section>
  );
};

export default SignalPanel;
