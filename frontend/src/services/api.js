const FLASK_BASE_URL = 'http://localhost:5000';
const JAVA_BASE_URL = 'http://localhost:8080';

export const uploadVideos = async (files) => {
  const formData = new FormData();
  formData.append('lane_1', files.lane_1);
  formData.append('lane_2', files.lane_2);
  formData.append('lane_3', files.lane_3);
  formData.append('lane_4', files.lane_4);

  const response = await fetch(`${FLASK_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Upload failed');
  }

  return response.json();
};

export const fetchTrafficState = async () => {
  const response = await fetch(`${JAVA_BASE_URL}/traffic/state`);
  if (!response.ok) {
    throw new Error('Failed to fetch traffic state');
  }
  return response.json();
};

export const getVideoFeedUrl = (laneId) => {
  return `${FLASK_BASE_URL}/video_feed/${laneId}`;
};
