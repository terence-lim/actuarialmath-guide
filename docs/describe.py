from inspect import signature
from actuarialmath.actuarial import Actuarial
from actuarialmath.interest import Interest
from actuarialmath.life import Life
from actuarialmath.survival import Survival
from actuarialmath.lifetime import Lifetime
from actuarialmath.fractional import Fractional
from actuarialmath.insurance import Insurance
from actuarialmath.annuity import Annuity
from actuarialmath.premiums import Premiums
from actuarialmath.policyvalues import PolicyValues, Contract
from actuarialmath.reserves import Reserves
from actuarialmath.recursion import Recursion
from actuarialmath.lifetable import LifeTable
from actuarialmath.sult import SULT
from actuarialmath.selectlife import SelectLife
from actuarialmath.mortalitylaws import MortalityLaws, Beta, Uniform, Makeham, Gompertz
from actuarialmath.constantforce import ConstantForce
from actuarialmath.extrarisk import ExtraRisk
from actuarialmath.mthly import Mthly
from actuarialmath.udd import UDD
from actuarialmath.woolhouse import Woolhouse

_methods = {
    Actuarial: ['solve', 'add_term', 'max_term', 'isclose'],
    Interest: ['annuity', 'mthly', 'double_force', ],
    Life: ['variance', 'covariance', 'bernoulli', 'binomial', 'mixture',
           'conditional_variance', 'portfolio_percentile', 'set_interest',
           'quantiles_frame'],
    Survival: ['set_survival', 'l_x', 'd_x', 'p_x', 'q_x', 'f_x', 'mu_x'],
    Lifetime: ['e_x'],
    Fractional: ['l_r', 'p_r', 'q_r', 'mu_r', 'f_r', 'E_r', 'e_r', 'e_approximate'],
    Insurance: ['E_x', 'A_x', 'insurance_variance', 'whole_life_insurance', 
                'term_insurance', 'deferred_insurance', 'endowment_insurance', 
                'increasing_insurance', 'decreasing_insurance', 'Z_x', 'Z_t',
                'Z_from_t', 'Z_from_prob', 'Z_to_t', 'Z_to_prob', 'Z_plot'],
    Annuity: ['a_x', 'immediate_annuity', 'annuity_twin', 'insurance_twin',
              'annuity_variance', 'whole_life_annuity', 'temporary_annuity',
              'deferred_annuity', 'certain_life_annuity', 'increasing_annuity',
              'decreasing_annuity', 'Y_x', 'Y_t', 'Y_from_t', 'Y_from_prob',
              'Y_to_t', 'Y_to_prob', 'Y_plot'],
    Premiums: ['net_premium', 'insurance_equivalence',
               'annuity_equivalence', 'premium_equivalence', 'gross_premium'],
    Contract: ['set_contract', 'premium_terms', 'renewal_profit', 'initial_cost',
               'claims_cost', 'renewals'],
    PolicyValues: ['gross_policy_value', 'gross_policy_variance',
                   'net_policy_value', 'net_policy_variance', 
                   'net_future_loss', 'gross_future_loss',
                   'net_variance_loss', 'gross_variance_loss',
                   'L_from_t', 'L_from_prob',
                   'L_to_t', 'L_to_prob', 'L_plot'],
    Reserves: ['set_reserves', 'fill_reserves', 't_V_forward', 
               't_V_backward', 't_V', 'r_V_forward', 'r_V_backward',
               'FPT_premium', 'FPT_policy_value', 'V_plot', 'reserves_frame'],    
    LifeTable: ['set_table', 'fill_table',  'frame', '__getitem__'],
    SULT: ['frame', '__getitem__'],
    SelectLife: ['set_table', 'set_select', 'fill_table', '__getitem__',
                 'frame', 'l_x', 'p_x', 'q_x', 'e_x', 'A_x', 'a_x'],
    Recursion: ['set_q', 'set_p', 'set_e', 'set_E', 'set_A', 'set_IA',
                'set_DA', 'set_a', 'blog_options'],
    MortalityLaws: ['l_r', 'p_r', 'q_r', 'mu_r', 'f_r', 'e_r'],
    ConstantForce: ['e_x', 'E_x', 'whole_life_insurance', 'temporary_annuity',
                    'term_insurance', 'Z_t', 'Y_t'],
    ExtraRisk: ['q_x', 'p_x', '__getitem__'],
    Mthly: ['v_m', 'p_m', 'q_m', 'Z_m', 'E_x', 'A_x',
            'whole_life_insurance', 'term_insurance', 'deferred_insurance',
            'endowment_insurance', 'immediate_annuity', 'insurance_twin',
            'annuity_twin', 'annuity_variance', 'whole_life_annuity',
            'temporary_annuity', 'deferred_annuity', 'immediate_annuity'],
    UDD: ['alpha', 'beta', 'interest_frame'],
    Woolhouse: ['mu_x'],
}


def methods(cls):
    """Helper to partially display docstrings from classes and methods"""
    s = "\nclass " + cls.__name__ + " - "
    s += "\n".join([l for l in cls.__doc__.strip().split('\n')]) + "\n"
    if cls in _methods and _methods[cls]:
        s += '\n    Methods:\n    --------\n\n'
        for method in _methods[cls]:
            meth = getattr(cls, method)
            desc = meth.__doc__.strip().split('\n')[0]
            if callable(meth):
                args = [str(arg) for arg in signature(meth).parameters.keys()
                        if str(arg) not in ['cls', 'self']]
            else:
                args = []
            s += f"    {method}(" + ", ".join(args) + f"):\n{' '*6}{desc}\n\n"
    print(s)

if False:
    print("Other usage examples")
    from actuarialmath.woolhouse import Woolhouse
    from actuarialmath.udd import UDD
    l = [110, 100, 92, 74, 58, 38, 24, 10, 0]
    table = LifeTable().set_interest(i=0.06)\
                       .set_table(l={age:l for age, l in zip(range(79, 88), l)},
                                  maxage=87)
                       
    print(table.mu_x(80))
    woolhouse = Woolhouse(life=table, m=4, three_term=True)
    print(woolhouse.whole_life_annuity(80)) # 3.1778
    print(woolhouse.immediate_annuity(80)) # 2.9278
    udd = UDD(life=table, m=4)
    print(udd.temporary_annuity(80, t=4)) # 2.7457
    
    l = [100, 90, 70, 50, 40, 20, 0]
    table = LifeTable().set_interest(i=0.08)\
                       .set_table(l={age:l for age, l in zip(range(70, 77), l)},
                                  maxage=76)                       
    print(table.A_x(70),
          table.A_x(70, moment=2))  # .75848, .58486
    print(table.endowment_insurance(70, t=3)) # .81974
    print('*', table.endowment_insurance(70, t=3, discrete=False)) # .81974

    print(table.E_x(70, t=3)) # .39692
    print('*', table.term_insurance(70, t=3, discrete=False)) # .43953
    print('*', table.endowment_insurance(70, t=3, discrete=False)) # .83644
    print(table.E_x(70, t=3, moment=2)) # .31503
    print('*', table.term_insurance(70, t=3, moment=2, discrete=False)) # .38786
    print('*', table.endowment_insurance(70, t=3, moment=2, discrete=False)) # .70294


    l = [1000, 990, 975, 955, 925, 890, 840]
    table = LifeTable().set_interest(i=0.08)\
                       .set_table(l={age:l for age,l in zip(range(70, 77), l)},
                                  maxage=76)                       
    print(table.increasing_annuity(70, t=4, discrete=True))
    print(table.decreasing_annuity(71, t=5, discrete=False))

    print('*', table.endowment_insurance(70, t=3, discrete=False)) # .7976

    l = [100, 90, 70, 50, 40, 20, 0]
    table = LifeTable().set_table(l={age:l for age,l in zip(range(70, 77), l)},
                                  maxage=76)\
                       .set_interest(i=0.08)
    print(1e6*table.whole_life_annuity(70, variance=True)) #1743784


    table = {x:l for x,l in zip(range(52,61), [89948,89089,88176,87208,86181,
                                               85093,83940,82719,81429])}
    life1 = LifeTable(udd=True).set_table(l=table)
    life2 = LifeTable(udd=False).set_table(l=table)
    print(life1.q_r(x=52, r=0.4, t=0.2))   # 0.001917
    print(life2.q_r(x=52, r=0.4, t=0.2))   # 0.001917
    print(life1.p_r(x=52, r=0.4, t=5.7))   # 0.935422
    print(life2.p_r(x=52, r=0.4, t=5.7))   # 0.935423
    print(life1.q_r(x=52, r=0.4, u=3.2, t=2.5))  # 0.030957
    print(life2.q_r(x=52, r=0.4, u=3.2, t=2.5))  # 0.030950
    #LifeTable.methods()
    
    
    
    print("Other examples")
    life = ConstantForce(mu=0.03).set_interest(delta=0.04)
    print(life.whole_life_annuity(20, discrete=False))  # 14.286
    print(life.temporary_annuity(20, t=5, discrete=False))  # 4.219


    life = ConstantForce(mu=.03).set_interest(delta=.04)
    print(life.E_x(20, t=5))  # .7047
    print(life.whole_life_insurance(20, discrete=False))  # .4286
    print(life.term_insurance(20, t=5, discrete=False))  # .1266
    print(life.endowment_insurance(20, t=5, discrete=False))  # .8313
    print(life.deferred_insurance(20, u=5, discrete=False))  # .3020

    life1 = ConstantForce(mu=.04).set_interest(delta=.02)
    life2 = ConstantForce(mu=.05).set_interest(delta=.02)
    life3 = ConstantForce(mu=.05).set_interest(delta=.03)

    A1 = life1.term_insurance(0, t=5, discrete=False)
    E1 = life1.E_x(0, t=5)
    A2 = life2.term_insurance(5, t=7, discrete=False)
    E2 = life2.E_x(5, t=7)
    A3 = life3.whole_life_insurance(12, discrete=False) 
    print(A1, E1, A2, E2, A1 + E1 * (A2 + E2 * A3))


    life = ConstantForce(mu=.04).set_interest(delta=.06)
    A1 = 10 * life.deferred_insurance(0, u=5, discrete=False)
    A2 = 10 * 10 * life.deferred_insurance(0, u=5, moment=2, discrete=False)
    E = 100 * A1
    V = 100 * (A2 - A1**2)
    print(A1, A2, E, V)  # 2.426, 11.233, 242.6, 534.8
    print(E + norm.ppf(0.95) * math.sqrt(V)) # 281

    print("Other usage examples")
    print(sult.temporary_annuity(80, t=10)*20000) # ~130770

    E = sult.E_x(60, t=5)
    print(E, E*sult.a_x(65, benefit=(lambda x,t: 1000 + .05*t)))

    print(sult.whole_life_annuity(60))  # 14.9041
    print(sult.whole_life_annuity(60, discrete=False))  # ~13.9041
    print(sult.deferred_annuity(60, u=10))  #6.9485
    print(sult.temporary_annuity(60, t=10))  # 7.9555
    print(sult.temporary_annuity(60, t=15))  # 10.5282
    print(sult.temporary_annuity(60, t=10))
    print(sult.E_x(60, t=10))  #
    print(sult.temporary_annuity(60, t=10, discrete=False))  # ~7.5341
    print(sult.certain_life_annuity(60, u=10))  # 15.0563
    print(sult.whole_life_annuity(60, variance=True, discrete=False)) # ~10.6182
    print(sult.endowment_insurance(60, t=10)) # .62116
    print(sult.whole_life_insurance(60, moment=2)) # .10834
    print(sult.whole_life_insurance(70, moment=2)) # .21467
    print(sult.endowment_insurance(60, t=10, moment=2)) # .38732
    print(sult.temporary_annuity(60, t=10, variance=True)) #.6513


    print(sult.p_x(70)) # 0.989587
    print(math.log(sult.p_x(70, t=2)) / -2)  # 0.011103

    A1 = sult.whole_life_insurance(20, discrete=False)
    #print(A1, sult.whole_life(20))
    A2 = sult.whole_life_insurance(50, discrete=False)
    #print(A2, sult.whole_life(50))
    A3 = sult.whole_life_insurance(70, discrete=False)
    E2 = sult.E_x(20, t=30)
    E3 = sult.E_x(20, t=50)
    print(A1, E2, A2, E3, A3, 125*A1 + E2*175*A2 - E3*250*A3)  # 5,335

    print(sult.whole_life_insurance(50)) # .18931
    print(sult.term_insurance(50, t=20)) # .0402
    print(sult.endowment_insurance(50, t=20))  # ~.31471
    print(sult.E_x(50, t=20), 
          sult.whole_life_insurance(70),
          sult.deferred_insurance(50, u=20)) # .14911

    print(sult.whole_life_insurance(50, discrete=False)) # .19400
    print(sult.term_insurance(50, t=20, discrete=False)) # .0412
    print(sult.endowment_insurance(50, t=20, discrete=False))  #.38944
    print(sult.E_x(50, t=20), 
          sult.whole_life_insurance(70, discrete=False),
          sult.deferred_insurance(50, u=20, discrete=False)) # .15281
  
    print("Other usage")
    mu = 0.04
    delta = 0.06
    life = Annuity().set_interest(delta=delta)\
                    .set_survival(mu=lambda *x: mu)
    print(life.temporary_annuity(50, t=20, b=10000, discrete=False))
    print(life.endowment_insurance(50, t=20, b=10000, discrete=False))
    print(life.E_x(50, t=20))
    print(life.whole_life_annuity(50, b=10000, discrete=False))
    print(life.whole_life_annuity(70, b=10000, discrete=False))

    mu = 0.07
    delta = 0.02
    life = Annuity().set_interest(delta=delta)\
                    .set_survival(mu=lambda *x: mu)
    print(life.whole_life_annuity(0, discrete=False) * 30)   # 333.33
    print(life.temporary_annuity(0, t=10, discrete=False) * 30)  # 197.81
    print(life.interest.annuity(5, m=0))  # 4.7581
    print(life.deferred_annuity(0, u=5, discrete=False)) # 7.0848
    print(life.certain_life_annuity(0, u=5, discrete=False))  # 11.842

    mu = 0.02
    delta = 0.05
    life = Annuity().set_interest(delta=delta)\
                    .set_survival(mu=lambda *x: mu)
    print(life.decreasing_annuity(0, t=5, discrete=False))  # 6.94
    
