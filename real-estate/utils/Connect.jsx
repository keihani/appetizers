import mongoose from 'mongoose'

 async function Connect() {
  if(mongoose.connection[0].readyState) return;
  try {
    await mongoose.connect(process.env.URL)
    console.log("Connect to DB");
  } catch (error) {
    console.log(error)
  }
}

export default Connect
