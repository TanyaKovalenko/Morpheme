#include <string>
#include <fstream>
#include <iostream>
#include <time.h>
#include <vector>
#include <unordered_set>

long write(std::string  to_check, std::string s, std::ofstream & out, std::unordered_set<std::string> & etalon_h, std::unordered_set<std::string> & already_h)
{
    if (already_h.find(to_check) == already_h.end() &&
        etalon_h.find(to_check) != etalon_h.end())
    {
        out << to_check << " : " << s << std::endl;
        return 1;
    }
    
    return 0;
}

int main()
{
    std::ifstream pre, end, root, suf, etalon, already;
    pre.open("prefixes");
    root.open("roots");
    suf.open("suffixes_");
    end.open("endings_");
    etalon.open("etalon");
    already.open("init");
    
    std::ofstream out;
    out.open("result_4");

    std::string line;

    std::vector<std::string> pre_v, suf_v, end_v, root_v;
   
    std::unordered_set<std::string> already_h; 
    std::unordered_set<std::string> etalon_h;

    long count = 0;
    double result = 0.1;
    clock_t t, cum_t;
    
    while( getline(pre, line) )
    {
        pre_v.push_back(line);
    }

    while( getline(root, line) )
    {
        root_v.push_back(line);
    }

    while( getline(suf, line) )
    {
        suf_v.push_back(line);
    }

    while( getline(end, line) )
    {
        end_v.push_back(line);
    }

    while( getline(etalon, line) )
    {
        etalon_h.insert(line);
    }

    while( getline(already, line) )
    {
         already_h.insert(line);
    }

    std::cout << etalon_h.size() << std::endl;

    typedef std::vector<std::string>::iterator iterator;
    cum_t = clock();

    long hit = 0;
    bool flag = false;

    std::string to_check, to_write;

    for(iterator it = root_v.begin(); it != root_v.end(); ++it) {
                for (iterator it4 = end_v.begin(); it4 != end_v.end(); ++it4) {
                    to_check = *it + *it4; to_write = *it +  ",-" + *it4;
                    if (etalon_h.find(to_check) != etalon_h.end())
                    {
                        out << to_check << " : " << to_write << std::endl;
                        etalon_h.erase(to_check);
                        ++hit;
                    }

                    count += 1;
                }
    }

    out.close();

    //std::cout << pre_v.size() << " " << end_v.size() << " " << root_v.size() << std::endl;

    pre.close();
    root.close();
    suf.close();
    end.close();
    etalon.close();
    already.close();

    return 0;
}
