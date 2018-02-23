#include <bits/stdc++.h>
using namespace std;
#define p 1000000007
void updateBIT(long long int BITree[],long long int n,long long int index,long long int val)
{
                    // index in BITree[] is 1 more than the index in arr[]
    index = index + 1;

                    // Traverse all ancestors and add 'val'
    while (index <= n)
    {
        // Add 'val' to current node of BI Tree
        BITree[index] +=val;
                        // Update index to that of parent in update View
        index += index & (-index);
    }
}

                // Constructs and returns a Binary Indexed Tree for given
                // array of size n.
long long *constructBITree(long long int arr[],long long int n)
{
                    // Create and initialize BITree[] as 0
    long long int *BITree = new long long int[n+1];
    for (int i=1; i<=n; i++)
        BITree[i] = 0;

        // Store the actual values in BITree[] using update()
    for (int i=0; i<n; i++)
        updateBIT(BITree, n, i, arr[i]);

    // Uncomment below lines to see contents of BITree[]
    //for (int i=1; i<=n; i++)
//      cout << BITree[i] << " ";

    return BITree;
}

    // SERVES THE PURPOSE OF getElement()
    // Returns sum of arr[0..index]. This function assumes
    // that the array is preprocessed and partial sums of
    // array elements are stored in BITree[]
long long getSum(long long int BITree[], long long int index)
{
    long long int sum = 0; // Iniialize result

                    // index in BITree[] is 1 more than the index in arr[]
    index = index + 1;

                    // Traverse ancestors of BITree[index]
    while (index>0)
    {
                        // Add current element of BITree to sum
        sum += BITree[index];

                        // Move index to parent node in getSum View
        index -= index & (-index);
    }
    return sum;
}

                // Updates such that getElement() gets an increased
                // value when queried from l to r.
void update(long long int BITree[], long long int l,long long  int r,long long  int n,long long  int val)
{
    // Increase value at 'l' by 'val'
    updateBIT(BITree, n, l, val%p);

    // Decrease value at 'r+1' by 'val'
    updateBIT(BITree, n, r+1,p-(val%p));
}
int main()
{
    //long long int t;
 //   cin>>t;
    long long int n,m;
    //while(t--)
    //{
        cin>>n>>m;
        long long int a[m+1],b[m+1],ty[m+1],r[m+1],l[m+1];
        memset(b,0,sizeof(b));
        memset(a,0,sizeof(a));
        memset(l,0,sizeof(l));
        memset(r,0,sizeof(r));
        memset(ty,0,sizeof(ty));
        for(int i=1;i<=m;i++)
        {
            cin>>ty[i]>>l[i]>>r[i];
        }
        long long int *BITree = constructBITree(a, m+1);
        update(BITree, 1,m+1,m+1, 1);
        for(int i=m;i>=1;i--)
        {
            if(ty[i]==2)
            {
                long long int value=(p+getSum(BITree,i))%p;
                update(BITree, l[i], r[i],m+1, value);
            }
        }
        for(int i=1;i<=m;i++)
        {
            if(ty[i]==1)
            {
                long long int value=(p+getSum(BITree,i))%p;
                b[l[i]-1]=((p+b[l[i]-1])%p+value%p)%p;
                if(r[i]<n)
                {
                    b[r[i]]=((p+b[r[i]]-value)%p);
                }
                //update(BITree1, l[i], r[i],m+1, value);
            }
        }
        for(int i=1;i<n;i++)
        {
            b[i]=(((p+b[i])%p)+(b[i-1]+p)%p)%p;
        }
        for(int i=0;i<n;i++)
        {
            cout<<b[i]<<" ";
        }
    //}
}
