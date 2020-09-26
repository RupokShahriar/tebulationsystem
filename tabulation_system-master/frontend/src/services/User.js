export default class User{
    async clearData()
    {
        window.localStorage.clear();
    }

    getUser(){
        try{
            const userDataString  = window.localStorage.getItem("@Tabulation:userData");

            if (!userDataString)
            {
                return false;
            }
            const user = JSON.parse(userDataString);
            return user;
        }
        catch(error)
        {
            return false;
        }
    }

    async storeUser(user)
    {
        const userData = JSON.stringify(user);
        console.log(userData);
        window.localStorage.setItem("@Tabulation:userData", userData);
    }
}