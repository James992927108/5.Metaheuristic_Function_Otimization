/* Declaration for random number related variables and routines */

# ifndef _RAND_H
# define _RAND_H

# include "global.h"

/* Variable declarations for the random number generator */
long double seed;
long double oldrand[55];
int jrand;
int rndcalcflag;
long double rndx1, rndx2;

/* Function declarations for the random number generator */
void randomize();
void warmup_random (long double seed);
void advance_random ();
long double randomperc();
int rnd (int low, int high);
long double rndreal (long double low, long double high);
void initrandomnormaldeviate();
long double noise (long double mu, long double sigma);
long double randomnormaldeviate();

# endif
