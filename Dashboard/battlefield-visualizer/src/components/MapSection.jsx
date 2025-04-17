import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import { motion } from 'framer-motion';
import drone from "../assets/drone-icon.png";
import 'leaflet/dist/leaflet.css';
import { useState, useEffect } from 'react';

const DroneAnimation = ({ paths }) => {
  const [currentPathIndex, setCurrentPathIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    if (currentPathIndex < paths.length - 1 && isAnimating) {
      const timer = setTimeout(() => {
        setCurrentPathIndex(prev => prev + 1);
      }, 2000);

      return () => clearTimeout(timer);
    } else if (currentPathIndex === paths.length - 1) {
      setTimeout(() => {
        setCurrentPathIndex(0);
      }, 3000);
    }
  }, [currentPathIndex, paths.length, isAnimating]);

  const currentPosition = paths[currentPathIndex];
  const nextPosition = paths[Math.min(currentPathIndex + 1, paths.length - 1)];

  return (
    <motion.img
      src={drone}
      alt="drone"
      className="drone-icon"
      style={{
        position: 'absolute',
        zIndex: 1000
      }}
      initial={{
        left: `${currentPosition[1]}%`,
        top: `${currentPosition[0]}%`,
      }}
      animate={{
        left: `${nextPosition[1]}%`,
        top: `${nextPosition[0]}%`,
      }}
      transition={{
        duration: 2,
        ease: "linear"
      }}
    />
  );
};

const MapSection = ({ satellite }) => {
  const positionA = [28.6139, 77.2090]; // Delhi
  const positionB = [28.7041, 77.1025]; // Example point
  const positionC = [28.65, 77.25]; // Another point
  const positionD = [28.68, 77.15]; // Another point

  const path1 = [positionA, positionB];
  const path2 = [positionB, positionC];
  const path3 = [positionC, positionD];
  const allPaths = [positionA, positionB, positionC, positionD];

  return (
    <div className="map-section">
      <div className="map-container">
        <MapContainer center={positionA} zoom={13} style={{ height: "400px", width: "100%" }}>
          <TileLayer
            url={satellite
              ? "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
              : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}
          />
          <Marker position={positionA} />
          <Marker position={positionB} />
          <Marker position={positionC} />
          <Marker position={positionD} />
          <Polyline pathOptions={{ color: '#6d5aee', weight: 3 }} positions={path1} />
          <Polyline pathOptions={{ color: '#00d9b8', weight: 3 }} positions={path2} />
          <Polyline pathOptions={{ color: '#ff6b6b', weight: 3 }} positions={path3} />
        </MapContainer>
        <div className="drone-overlay">
          <DroneAnimation paths={allPaths} />
        </div>
      </div>
    </div>
  );
};

export default MapSection;