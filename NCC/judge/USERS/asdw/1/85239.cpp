#include<bits/stdc++.h>
using namespace std;
int main()
{
	long long  t;
	cin>>t;
	while(t--)
	{
		long long  n,mi=LLONG_MAX,ma=LLONG_MIN;
		cin>>n;
		vector<long long >arr(n);
		for(long long  i=0;i<n;i++)
			cin>>arr[i];
		for(long long i=0;i<n;i++)
		{
			mi=min(mi,arr[i]);
			ma=max(ma,arr[i]);
		}
		cout<<ma-mi<<"\n";
	}
}
