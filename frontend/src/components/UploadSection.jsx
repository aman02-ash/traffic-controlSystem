import React, { useState } from 'react';

const UploadSection = ({ onUpload, status }) => {
  const [files, setFiles] = useState({
    lane_1: null,
    lane_2: null,
    lane_3: null,
    lane_4: null,
  });

  const handleFileChange = (lane, e) => {
    setFiles((prev) => ({ ...prev, [lane]: e.target.files[0] }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!files.lane_1 || !files.lane_2 || !files.lane_3 || !files.lane_4) {
      alert('Please select videos for all 4 lanes.');
      return;
    }
    onUpload(files);
  };

  return (
    <section className="upload-section">
      <h2>Upload Traffic Videos</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-inputs">
          {['lane_1', 'lane_2', 'lane_3', 'lane_4'].map((lane) => (
            <div key={lane} className="file-input-group">
              <label htmlFor={lane}>{lane.replace('_', ' ').toUpperCase()}</label>
              <input
                type="file"
                id={lane}
                accept="video/*"
                onChange={(e) => handleFileChange(lane, e)}
              />
            </div>
          ))}
        </div>
        <button type="submit" disabled={status === 'uploading'}>
          {status === 'uploading' ? 'Uploading...' : 'Upload All Videos'}
        </button>
        {status !== 'idle' && <p className={`status-msg ${status}`}>{status.toUpperCase()}</p>}
      </form>
    </section>
  );
};

export default UploadSection;
