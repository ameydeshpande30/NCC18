#include <bits/stdc++.h>

using namespace std;

int minimumAbsoluteDifference(int n, vector <int> arr) {
    int min,diff;
    
    sort(arr.begin(),arr.begin()+n);
    min=arr[n-1]-arr[0];
    for(int i=0;i<n;i++)
    {
        for(int j=i+1;j<n;j++)
        {
            diff=arr[j]-arr[i];
            if(diff<min)
            {
                min=diff;
            }
            else if(diff>=min)
                break;
        }
    }
   return min;
    // Complete this function
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for(int arr_i = 0; arr_i < n; arr_i++){
       cin >> arr[arr_i];
    }
    int result = minimumAbsoluteDifference(n, arr);
    cout << result << endl;
    return 0;
}
