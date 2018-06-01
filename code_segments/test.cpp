#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>

#include <opencv2/opencv.hpp>
int main()
{
    std::ifstream infile("../rotation_vector.txt");
    std::string line;
    int line_index = 0;
    while(std::getline(infile, line))
    {
        boost::replace_all(line, "\n", "");
        std::vector<std::string> tokens;
        boost::split(tokens, line, boost::is_any_of(" "));

        float w = boost::lexical_cast<float>(tokens[0]);
        float x = boost::lexical_cast<float>(tokens[1]);
        float y = boost::lexical_cast<float>(tokens[2]);
        float z = boost::lexical_cast<float>(tokens[3]);


      //  cv::Mat rodVec(3, 1, CV_32F);
      //  rodVec.at<float>(0, 0) = x * w;
      //  rodVec.at<float>(1, 0) = y * w;
      //  rodVec.at<float>(2, 0) = z * w;

        cv::Mat rotation;
        //cv::Rodrigues(rodVec, rotation);
        //std::cout << rotation << std::endl;

        cv::Vec3f rVec(x * w, y * w, z * w);
        cv::Rodrigues(rVec, rotation);
        std::cout << line_index++ << std::endl;
        std::cout << rotation << std::endl;

    }
}