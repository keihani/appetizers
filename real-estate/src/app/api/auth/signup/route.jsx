import { NextResponse } from 'next/server';
import Connect from '@/utils/Connect';
import User from '@/models/User';
import { HashPassword } from '@/utils/operations/Password';

export async function POST(req) {
  try {
    const {email, password} = await req.json()
    if(!email || !password)
        return NextResponse.json({status: 422, message: "Please fill all fields"})
    await Connect()
    const user = await User.findOne({email})
    if(user)
        return NextResponse.json({status: 401, message: "You are registered before!"})

    const hashedPassword = await HashPassword(password)
    const newUser = User.create({email, password: hashedPassword})
    return NextResponse.json({status:201, message:"You registered successfully. Thank you.", data: newUser})

  } catch (error) {
    console.log(error);
    return NextResponse.json({status:500, message:"Server Error!"})
  }
}
