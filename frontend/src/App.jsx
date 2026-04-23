import React, { useState, useEffect } from 'react';
import UploadSection from './components/UploadSection';
import SignalPanel from './components/SignalPanel';
import LaneCard from './components/LaneCard';
import SummaryPanel from './components/SummaryPanel';
import { uploadVideos, fetchTrafficState } from './services/api';

const App = () => {
  const [uploadStatus, setUploadStatus] = useState('idle');
  const [trafficState, setTrafficState] = useState(null);
  const [isLive, setIsLive] = useState(false);

  const handleUpload = async (files) => {
    setUploadStatus('uploading');
    try {
      await uploadVideos(files);
      setUploadStatus('success');
      setIsLive(true);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
    }
  };

  useEffect(() => {
    let interval;
    if (isLive) {
      const poll = async () => {
        try {
          const state = await fetchTrafficState();
          setTrafficState(state);
        } catch (error) {
          console.error('Polling error:', error);
        }
      };
      poll();
      interval = setInterval(poll, 2000);
    }
    return () => clearInterval(interval);
  }, [isLive]);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Smart Traffic Control System</h1>
        <div className="system-status">
          <span className={`status-dot ${isLive ? 'live' : 'offline'}`}></span>
          {isLive ? 'SYSTEM LIVE' : 'SYSTEM OFFLINE'}
        </div>
      </header>

      <main className="dashboard-grid">
        <div className="left-column">
          <UploadSection onUpload={handleUpload} status={uploadStatus} />
          <SignalPanel
            activeGreenLane={trafficState?.activeGreenLane}
            timer={trafficState?.timer}
            mode="Adaptive Signal Control"
          />
          <SummaryPanel trafficState={trafficState} />
        </div>

        <div className="right-column">
          <div className="lanes-grid">
            {['lane_1', 'lane_2', 'lane_3', 'lane_4'].map((laneId) => (
              <LaneCard
                key={laneId}
                laneId={laneId}
                laneData={trafficState?.laneStates?.[laneId]}
                isActive={trafficState?.activeGreenLane === laneId}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
