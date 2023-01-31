import aws from "../assets/img/aws.png";
import python from "../assets/img/python.png";
import csharp from "../assets/img/csharp.png";
import nodejs from "../assets/img/nodejs.png"
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import colorSharp from "../assets/img/color-sharp.png";

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
                        <p>I've learned a lot in school and on the job. Here are some of my top skills:<br></br></p>
                        <Carousel responsive={responsive} infinite={true} className="owl-carousel owl-theme skill-slider">
                            <div className="item">
                                <img src={aws} alt="aws" />
                                <h5>Cloud Development</h5>
                            </div>
                            <div className="item">
                                <img src={python} alt="Python" />
                                <h5>Python</h5>
                            </div>
                            <div className="item">
                                <img src={csharp} alt="C#" />
                                <h5>.NET</h5>
                            </div>
                            <div className="item">
                                <img src={nodejs} alt="Node.js" />
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
