import { motion } from "framer-motion";
import drone from "../assets/drone-icon.png";
import { useState, useEffect } from 'react';

const DroneAnimation = ({ paths }) => {
  const [currentPathIndex, setCurrentPathIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    if (currentPathIndex < paths.length - 1 && isAnimating) {
      const timer = setTimeout(() => {
        setCurrentPathIndex(prev => prev + 1);
      }, 2000); // Move to next point every 2 seconds

      return () => clearTimeout(timer);
    } else if (currentPathIndex === paths.length - 1) {
      // Reset after 3 seconds when reaching the end
      setTimeout(() => {
        setCurrentPathIndex(0);
      }, 3000);
    }
  }, [currentPathIndex, paths.length, isAnimating]);

  const currentPosition = paths[currentPathIndex];
  const nextPosition = paths[Math.min(currentPathIndex + 1, paths.length - 1)];

  return (
    <div className="drone-overlay">
      <motion.img
        src={drone}
        alt="drone"
        className="drone-icon"
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
    </div>
  );
};

export default DroneAnimation; 