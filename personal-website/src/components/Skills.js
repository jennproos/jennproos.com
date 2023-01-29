import meter1 from "../assets/img/meter1.svg";
import meter2 from "../assets/img/meter2.svg";
import meter3 from "../assets/img/meter3.svg";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import colorSharp from "../assets/img/color-sharp.png";
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

export const Skills = () => {
  const responsive = {
    superLargeDesktop: {
      // the naming can be any, depends on you.
      breakpoint: { max: 4000, min: 3000 },
      items: 5
    },
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1
    }
  };

  return (
    <section className="skill" id="skills">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="skill-bx wow zoomIn">
                        <h2>Skills</h2>
                        <p>I learned a lot in school and on the job. Here are some of my top skills:<br></br></p>
                        <Carousel responsive={responsive} infinite={true} className="owl-carousel owl-theme skill-slider">
                            <div className="item">
                                <CircularProgressbar
                                    value={80}
                                    text={`${80}%`}
                                    styles={buildStyles({
                                    })}
                                />
                                <h5>Cloud Development</h5>
                            </div>
                            <div className="item">
                                <CircularProgressbar
                                    value={85}
                                    text={`${85}%`}
                                    styles={buildStyles({
                                    })}
                                />
                                <h5>Python</h5>
                            </div>
                            <div className="item">
                                <CircularProgressbar
                                    value={90}
                                    text={`${90}%`}
                                    styles={buildStyles({
                                    })}
                                />
                                <h5>.NET</h5>
                            </div>
                            <div className="item">
                                <CircularProgressbar
                                    value={85}
                                    text={`${85}%`}
                                    styles={buildStyles({
                                    })}
                                />
                                <h5>Node.js</h5>
                            </div>
                        </Carousel>
                    </div>
                </div>
            </div>
        </div>
        <img className="background-image-left" src={colorSharp} alt="Image" />
    </section>
  )
}
