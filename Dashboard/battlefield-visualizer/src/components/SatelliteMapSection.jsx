// DroneOverlay.jsx
import drone from "../assets/drone-icon.png";
import { motion } from "framer-motion";

const SatelliteMapSection = () => (
  <div style={{ position: 'relative', height: '100px', marginTop: '-100px' }}>
    <motion.img
      src={drone}
      alt="drone"
      initial={{ x: 0 }}
      animate={{ x: "90vw" }}
      transition={{ duration: 6, repeat: Infinity, repeatType: "loop" }}
      style={{ height: '40px', position: 'absolute', top: 0 }}
    />
  </div>
);
export default SatelliteMapSection;