import awsCert from "../assets/img/aws-ccp-badge.png";
import azureCert from "../assets/img/azure-fundamentals-badge.png";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import colorSharp from "../assets/img/color-sharp.png";

export const Certifications = () => {
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
    <section className="certification" id="certifications">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="certification-bx wow zoomIn">
                        <h2>Certifications</h2>
                        <Carousel responsive={responsive} infinite={true} className="owl-carousel owl-theme certification-slider">
                            <div className="item">
                                <a href="https://www.credly.com/badges/d91f9693-dbfb-48a9-9856-5cbc222c62be/public_url" target="_blank">
                                  <img src={awsCert} alt="AWS Certified Cloud Practitioner Badge" />
                                </a>
                            </div>
                            <div className="item">
                                <a href="https://www.credly.com/badges/756a3c8a-c0a5-40f1-9de4-c99cbb8da9da/public_url" target="_blank">
                                    <img src={azureCert} alt="Azure Fundamentals Badge" />
                                </a>
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
