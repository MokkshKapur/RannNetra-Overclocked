// StaticImage.jsx
import image from "../assets/staticImage.jpg";

const StaticImageSection = () => (
  <section className="static-image">
    <img src={image} alt="Battlefield Situation" style={{ width: "100%", borderRadius: "8px" }} />
  </section>
);
export default StaticImageSection;
  