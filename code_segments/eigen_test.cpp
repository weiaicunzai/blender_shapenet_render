#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <Eigen/Geometry>

#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>

int main()
{
    std::ifstream ifile("rotation_quaternion.txt");

    std::string line;

    int line_index = 0;
    while(std::getline(ifile, line))
    {
        boost::replace_all(line, "\n", "");
        std::vector<std::string> tokens;
        boost::split(tokens, line, boost::is_any_of(" "));

        float w = boost::lexical_cast<float>(tokens[0]);
        float x = boost::lexical_cast<float>(tokens[1]);
        float y = boost::lexical_cast<float>(tokens[2]);
        float z = boost::lexical_cast<float>(tokens[3]);

         Eigen::Quaterniond q(w, x, y, z);
         q.normalize();
         Eigen::Matrix3d R = q.toRotationMatrix(); 

         std::cout << line_index++ << std::endl;
         std::cout << R << std::endl;
    }
}