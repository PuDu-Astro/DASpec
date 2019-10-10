#include "compcontainer.h"

compcontainer::compcontainer()
{
    ncomp = 0;
    npar = 0;
    nfix = 0;
    ntie = 0;
}

void compcontainer::add(component *c)
{
    comp[ncomp] = c;
    ncomp += 1;
    npar += c->npar;
}

void compcontainer::info()
{
    if (ncomp > 0) std::cout << "component:" << std::endl;
    for (int i = 0; i < ncomp; ++i)
    {
        std::cout << i + 1 << "= ";
        comp[i]->info();
    }
    //std::cout << std::endl;
    
    if (nfix > 0) std::cout << "fix:" << std::endl;
    for (int i = 0; i < nfix; ++i)
    {
        std::cout << i + 1 << "= ";
        std::cout << "comp:" << " " << fix[i][0] + 1 << " ";
        std::cout << "par:" << " " << fix[i][1] + 1 << " ";
        std::cout << "value: " << " " << fixval[i] << std::endl;
    }
    //std::cout << std::endl;
    
    if (ntie > 0) std::cout << "tie:" << std::endl;
    for (int i = 0; i < ntie; ++i)
    {
        std::cout << i + 1 << "= ";
        std::cout << "comp:" << " " << tie[i][0] + 1 << " ";
        std::cout << "par:" << " " << tie[i][1] + 1 << " ";
        std::cout << "target_comp:" << " " << tie[i][2] + 1 << " ";
        std::cout << "target_par:" << " " << tie[i][3] + 1 << " ";
        if (tie[i][4] == 0) std::cout << "type: ratio ";
        else if (tie[i][4] == 1) std::cout << "type: offset ";
        std::cout << "value: " << " " << tieval[i] << std::endl;
    }
}

void compcontainer::calc_totpar(int num, double *x, double *y, double *p)
{
    int n = 0;
        
    for (int i = 0; i < ncomp; ++i)
    {
        // update parameters in each component
        for (int j = 0; j < comp[i]->npar; ++j) comp[i]->par[j] = p[n + j];
        n += comp[i]->npar;
        
        // calculate the component
        comp[i]->calc(num, x, y, comp[i]->par);
    }
}

void compcontainer::parl2s(double *ptot, double *p)
{
    int nfree = 0, temp;
    for (int i = 0; i < npar; ++i)
    {
        temp = 0;
        for (int j = 0; j < nfix; ++j)
        {
            if (i == findpar(fix[j][0], fix[j][1])) temp = 1;
        }
        for (int j = 0; j < ntie; ++j)
        {
            if (i == findpar(tie[j][0], tie[j][1])) temp = 1;
        }
        if (temp == 0)
        {
            p[nfree] = ptot[i];
            nfree += 1;
        }
    }
}

void compcontainer::parerrs2l(double *p, double *ptot)
{
    int nfree = 0;
    int temp;
    
    for (int i = 0; i < npar; ++i)
    {
        ptot[i] = 0.0;
        temp = 0;
        for (int j = 0; j < nfix; ++j)
        {
            if (i == findpar(fix[j][0], fix[j][1])) temp = 1;
        }
        for (int j = 0; j < ntie; ++j)
        {
            if (i == findpar(tie[j][0], tie[j][1])) temp = 1;
        }
        if (temp == 0)
        {
            ptot[i] = p[nfree];
            nfree += 1;
        }
    }
}

void compcontainer::pars2l(double *p, double *ptot)
{
    int nfree = 0;
    int label[npar], temp;
    for (int i = 0; i < npar; ++i) label[i] = 0;
    
    for (int i = 0; i < npar; ++i)
    {
        temp = 0;
        for (int j = 0; j < nfix; ++j)
        {
            if (i == findpar(fix[j][0], fix[j][1])) temp = 1;
        }
        for (int j = 0; j < ntie; ++j)
        {
            if (i == findpar(tie[j][0], tie[j][1])) temp = 1;
        }
        if (temp == 0)
        {
            ptot[i] = p[nfree];
            label[i] = 1;
            nfree += 1;
        }
    }
    
    for (int i = 0; i < npar; ++i)
    {
        for (int j = 0; j < nfix; ++j)
        {
            if (i == findpar(fix[j][0], fix[j][1]))
            {
                ptot[i] = fixval[j];
                label[i] = 1;
            }
        }
        for (int j = 0; j < ntie; ++j)
        {
            if (i == findpar(tie[j][0], tie[j][1]))
            {
                //std::cout << tie[j][0] << tie[j][1] << tie[j][2] << tie[j][3] << std::endl;
                if (tie[j][4] == 0)
                {
                    //std::cout << tie[j][2] << tie[j][3] << std::endl;
                    //std::cout << findpar(tie[j][2], tie[j][3]) << std::endl;
                    //std::cout << ptot[findpar(tie[j][2], tie[j][3])] << std::endl;
                    ptot[i] = tieval[j] * ptot[findpar(tie[j][2], tie[j][3])];
                }
                else if (tie[j][4] == 1)
                {
                    //std::cout << ptot[findpar(tie[j][2], tie[j][3])] << std::endl;
                    ptot[i] = tieval[j] + ptot[findpar(tie[j][2], tie[j][3])];
                }
                label[i] = 1;
            }
        }
    }
    
    for (int i = 0; i < npar; ++i)
    {
        //std::cout << ptot[i] << " ";
        if (label[i] == 0)
        {
            std::cout << "Error! parameter is not assigned!";
        }
    }
    //std::cout << std::endl;
}

int compcontainer::findpar(int c, int p)
{
    int n = 0;
    
    for (int i = 0; i < c; ++i)
    {
        n += comp[i]->npar;
    }
    
    n += p;
    
    return n;
}

void compcontainer::calc(int num, double *x, double *y, double *p)
{
    double ptot[npar];
    pars2l(p, ptot);
    //for (int i = 0; i < npar; ++i) std::cout << ptot[i] << " ";
    //std::cout << std::endl;
    calc_totpar(num, x, y, ptot);
}

void compcontainer::clean()
{
    for (int i = 0; i < ncomp; ++i) delete comp[i];
    npar = 0;
    ncomp = 0;
    nfix = 0;
    ntie = 0;
}

//compcontainer::~compcontainer()
//{
//    for (int i = 0; i < ncomp; ++i) delete comp[i];
//    npar = 0;
//    ncomp = 0;
//    nfix = 0;
//    ntie = 0;
//}

void compcontainer::addfix(int c, int p, double val)
{
    c -= 1;
    p -= 1;
    
    if (c < 0 || c >= ncomp)
    {
        std::cout << "Fix Error! has no such comp: " << c << std::endl;
        std::exit(-1); 
    }
    if (p < 0 || p >= comp[c]->npar)
    {
        std::cout << "Fix Error! comp " << c << " has no such par: " << p << std::endl;
        std::exit(-1); 
    }
    
    fix[nfix][0] = c;
    fix[nfix][1] = p;
    fixval[nfix] = val;
    nfix += 1;
}

void compcontainer::addtie(int c, int p, int ct, int pt, std::string type, double val)
{
    c -= 1;
    p -= 1;
    ct -= 1;
    pt -= 1;
    
    if (c < 0 || c >= ncomp)
    {
        std::cout << "Tie Error! has no such comp: " << c << std::endl;
        std::exit(-1); 
    }
    if (p < 0 || p >= comp[c]->npar)
    {
        std::cout << "Tie Error! comp " << c << " has no such par: " << p << std::endl;
        std::exit(-1); 
    }
    if (ct < 0 || ct >= ncomp)
    {
        std::cout << "Tie Error! has no such comp: " << ct << std::endl;
        std::exit(-1); 
    }
    if (pt < 0 || pt >= comp[ct]->npar)
    {
        std::cout << "Tie Error! comp " << ct << " has no such par: " << pt << std::endl;
        std::exit(-1); 
    }
    for (int i = 0; i < ntie; ++i)
    {
        if ((c == tie[i][0]) && (p == tie[i][1]))
        {
            std::cout << "Tie Error! tie repeatly! comp: " << c << " par: " << p << std::endl;
            std::exit(-1);
        }
    }
    if ((c == ct) && (p == pt))
    {
        std::cout << "Tie Error! object and target are the same: "; 
        std::cout << "comp:" << c << " par: " << p;
        std::cout << " target_comp:" << ct << " target_par: " << pt << std::endl;
        std::exit(-1);
    }
    
    tie[ntie][0] = c;
    tie[ntie][1] = p;
    tie[ntie][2] = ct;
    tie[ntie][3] = pt;
    if (type == "ratio") tie[ntie][4] = 0;
    else if (type == "offset") tie[ntie][4] = 1;
    tieval[ntie] = val;
    ntie += 1;
}

void compcontainer::addtie_profile(int c, int ct)
{
    if (comp[c - 1]->profile != comp[ct - 1]->profile)
    {
        std::cout << "Tie Profile Error! not the same profile: component: " << c;
        std::cout << " component: " << ct << std::endl;
        std::exit(-1);
    }
    
    for (int i = 1; i < comp[c - 1]->npar; ++i) addtie(c, i + 1, ct, i + 1, "ratio", 1.0);
}

void compcontainer::addtie_flux_profile(int c, int ct, double val)
{
    if (comp[c - 1]->profile != comp[ct - 1]->profile)
    {
        std::cout << "Tie Profile Error! not the same profile: component: " << c;
        std::cout << " component: " << ct << std::endl;
        std::exit(-1);
    }

    addtie(c, 1, ct, 1, "ratio", val);
    for (int i = 1; i < comp[c - 1]->npar; ++i) addtie(c, i + 1, ct, i + 1, "ratio", 1.0);
}

int compcontainer::netnpar()
{
    return npar - nfix - ntie;
}
